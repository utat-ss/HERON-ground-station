import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper
import ax25

ping_delay = 3
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')

run = True
txer = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")

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

    t_pinger = Thread(target=pinger)
    t_rx_sink = Thread(target=rx_sink)
    t_pinger.start()
    t_rx_sink.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    t_rx_sink.join()
    