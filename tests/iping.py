import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ping_delay = 3
ping_msg = "ES+R2200\r"

pings_sent = 0
pings_rcvd = 0
run = True
txer = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
rxer = ESTTCWrapper("tcp://10.0.1.165:50491", "tcp://10.0.1.165:50492")

def txer_rx_sink():
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            txer.rx(zmq.NOBLOCK)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def rxer_rx_sink():
    global pings_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            msg = rxer.rx(zmq.NOBLOCK)
            if msg == ping_msg:
                pings_rcvd += 1
                print("ping received [{}]".format(pings_rcvd))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger():
    global pings_sent
    global pings_rcvd
    rxer.set_timeout(ping_delay*1000)
    while run:
        txer.tx(ping_msg)
        pings_sent += 1
        try:
            msg = rxer.rx()
            if msg == ping_msg:
                pings_rcvd += 1
                print("ping received [{}]".format(pings_rcvd))
        except zmq.ZMQError:
            print('timeout')

if __name__ == '__main__':
    t_txer_rx_sink = Thread(target=txer_rx_sink)
    t_pinger = Thread(target=pinger)

    t_txer_rx_sink.start()
    t_pinger.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    rxer_rx_sink()
    t_txer_rx_sink.join()

    total_loss = "{0:.2f} %".format((pings_sent-pings_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', pings_rcvd)
    print('  total loss:      ', total_loss)
    