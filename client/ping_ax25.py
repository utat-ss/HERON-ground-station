import time
from threading import Thread
import zmq
import ax25
import stations

ping_delay = 3
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')
freq = 436025000

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

    (trx, flow, digi, rot) = stations.setup_herongs(rot_config="lab", tx_config=int(80))

    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_mode(3)

    t_pinger = Thread(target=pinger, args=[digi,])
    t_rx_sink = Thread(target=rx_sink, args=[digi,])
    t_pinger.start()
    t_rx_sink.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    t_rx_sink.join()
    