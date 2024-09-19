import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper
import ax25

resp_timeout = 1
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')

pings_sent = 0
resps_rcvd = 0
run = True
pinger = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")

def rx_sink():
    global resps_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            resp = pinger.rx_bytes(zmq.NOBLOCK)
            if resp != ping_msg:
                resps_rcvd += 1
                print(ax25.pkt2str(resp))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger():
    global pings_sent
    global resps_rcvd
    pinger.set_timeout(resp_timeout*1000)
    while run:
        pinger.tx_bytes(ping_msg)
        pings_sent += 1
        try:
            resp = pinger.rx_bytes()
            if resp != ping_msg:
                resps_rcvd += 1
                print(ax25.pkt2str(resp))
        except zmq.ZMQError:
            print('\033[91mtimeout\033[0m')

if __name__ == '__main__':

    t_pinger = Thread(target=pinger)
    t_pinger.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    rx_sink()

    total_loss = "{0:.2f} %".format((pings_sent-resps_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', resps_rcvd)
    print('  total loss:      ', total_loss)
    