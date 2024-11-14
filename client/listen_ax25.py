import time
from threading import Thread
import zmq
import ax25
import stations

freq = 446_000_000

run = True

def rx_sink(txer):
    global resps_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            resp = txer.rx_bytes(zmq.NOBLOCK)
            try: print(ax25.pkt2str(resp))
            except: print(resp)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

if __name__ == '__main__':

    (client, channel, flow, digi, rot) = stations.setup_herongs(rot_config="lab")

    flow.set_cfo(freq + 100_000)
    flow.set_freq(freq)
    flow.set_mode(3)
    flow.set_output("/tmp/iping_test.fc32")

    t_rx_sink = Thread(target=rx_sink, args=[digi,])
    t_rx_sink.start()

    input("Press Enter to quit...\n")
    run = False

    t_rx_sink.join()
    