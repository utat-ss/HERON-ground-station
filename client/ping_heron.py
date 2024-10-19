import time
from threading import Thread
import zmq
from xmlrpc.client import ServerProxy
import stations

ping_delay = 3
ping_msg = "ES+R2200\r"
norad = 58326
freq = 435_000_000

run = True

def rx_sink(txer):
    global resps_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            resp = txer.rx(zmq.NOBLOCK)
            print(resp)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger(txer):
    while run:
        txer.tx(ping_msg)
        time.sleep(ping_delay)

if __name__ == '__main__':
    
    (trx, flow, digi, rot) = stations.setup_herongs(rot_config=int(norad), tx_config=int(80))

    print(rot.get_tracking_status())

    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_mode(1)

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
    