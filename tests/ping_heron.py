import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper
from xmlrpc.client import ServerProxy
import ax25

ping_delay = 3
ping_msg = "ES+R2200\r"

run = True
txer = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
flow = ServerProxy('http://10.0.7.91:8080')

def rx_sink():
    global resps_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            resp = txer.rx(zmq.NOBLOCK)
            print(resp)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger():
    while run:
        txer.tx(ping_msg)
        time.sleep(ping_delay)

if __name__ == '__main__':

    flow.set_cfo(435400000)
    flow.set_freq(435000000)
    flow.set_lna(True)
    flow.set_pa(True)
    flow.set_tx_pwr(80)
    flow.set_rx_vga_gain(62)
    flow.set_rx_if_gain(40)
    flow.set_rx_amp(True)
    flow.set_mode(1)

    t_pinger = Thread(target=pinger)
    t_rx_sink = Thread(target=rx_sink)
    t_pinger.start()
    t_rx_sink.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    t_rx_sink.join()
    