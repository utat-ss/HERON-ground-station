import time
from threading import Thread
import zmq
from xmlrpc.client import ServerProxy
import ax25
import stations

ping_delay = 3
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')
norad = 55098
freq = 436_025_000

run = True

def rx_sink(txer):
    global resps_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            resp = txer.rx_bytes(zmq.NOBLOCK)
            print(ax25.pkt2str(resp))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger(txer):
    while run:
        txer.tx_bytes(ping_msg)
        time.sleep(ping_delay)

if __name__ == '__main__':

    (trx, flow, digi, rot) = stations.setup_herongs(rot_config=int(norad), tx_config=int(80))

    print(rot.get_tracking_status())

    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_mode(3)

    dpler = ServerProxy(f"http://10.0.7.91:50600")
    dpler.load_norad(norad)
    dpler.set_freq(freq)
    dpler.enable_correction()

    t_pinger = Thread(target=pinger, args=[digi,])
    t_rx_sink = Thread(target=rx_sink, args=[digi,])
    t_pinger.start()
    t_rx_sink.start()

    input("Press Enter to quit...\n")
    run = False

    rot.disable_tracking()
    dpler.disable_correction()    
    t_pinger.join()
    t_rx_sink.join()
    