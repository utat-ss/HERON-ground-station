import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ping_delay = 3
ping_msg = "ES+R2200\r"

pings_sent = 0
pings_rcvd = 0
run = True
ping_esttc = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")

def ping_tx():
    global pings_sent
    while run:
        ping_esttc.tx(ping_msg)
        pings_sent += 1
        time.sleep(ping_delay)

def ping_rx():
    global pings_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            rx = ping_esttc.rx(zmq.NOBLOCK)
            if rx == ping_msg:
                pings_rcvd += 1
                print("--- ping received [{}]".format(pings_rcvd))
            else:
                print("--- received: {}".format(rx))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

if __name__ == '__main__':
    t_ping_rx = Thread(target=ping_rx)
    t_ping_tx = Thread(target=ping_tx)

    t_ping_rx.start()
    t_ping_tx.start()

    input("Press Enter to quit...\n")
    run = False

    t_ping_rx.join()
    t_ping_tx.join()

    total_loss = "{0:.2f} %".format((pings_sent-pings_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', pings_rcvd)
    print('  total loss:      ', total_loss)
    