import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ping_delay = 0.5
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
    while run:
        try:
            rx = ping_esttc.rx(zmq.NOBLOCK)
            if rx == ping_msg:
                print("--- ping received!")
                pings_rcvd += 1
            else:
                print("--- weird ping: ", rx)
        except zmq.ZMQError:
            continue

if __name__ == '__main__':
    t_ping_rx = Thread(target=ping_rx)
    t_ping_tx = Thread(target=ping_tx)

    t_ping_rx.start()
    t_ping_tx.start()

    input("Press Enter to quit...")
    run = False

    t_ping_rx.join()
    t_ping_tx.join()

    total_loss = "{0:.2f} %".format((pings_sent-pings_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', pings_rcvd)
    print('  total loss:      ', total_loss)
    