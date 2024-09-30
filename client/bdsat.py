import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper
from xmlrpc.client import ServerProxy
import ax25
import rpyc

ping_delay = 3
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')

run = True
txer = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
flow = ServerProxy('http://10.0.7.91:8080')

def rx_sink():
    global resps_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            resp = txer.rx_bytes(zmq.NOBLOCK)
            print(ax25.pkt2str(resp))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger():
    while run:
        txer.tx_bytes(ping_msg)
        time.sleep(ping_delay)

if __name__ == '__main__':

    norad = 55098
    freq = 436_025_000
    ip = "10.0.7.91"

    rot = rpyc.connect(ip, 18866).root.K3NG
    rot.load_and_track(norad)
    rot.enable_tracking()
    print(rot.get_tracking_status())

    flow = ServerProxy(f"http://{ip}:8080")
    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_lna(True)
    flow.set_rx_vga_gain(62)
    flow.set_rx_if_gain(40)
    flow.set_rx_amp(True)
    flow.set_pa(True)
    flow.set_tx_pwr(80)
    flow.set_mode(3)

    dpler = ServerProxy(f"http://{ip}:50600")
    dpler.load_norad(norad)
    dpler.set_freq(freq)
    dpler.enable_correction()

    t_pinger = Thread(target=pinger)
    t_rx_sink = Thread(target=rx_sink)
    t_pinger.start()
    t_rx_sink.start()

    input("Press Enter to quit...\n")
    run = False

    rot.disable_tracking()
    dpler.disable_correction()    
    t_pinger.join()
    t_rx_sink.join()
    