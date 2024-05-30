import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ping_delay = 1
ping_msg = "ES+R2200\r"
pong_msg = "ACK"

pings = 0
pongs = 0
ping_pongs = 0
run = True
ping_esttc = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
pong_esttc = ESTTCWrapper("tcp://10.0.1.165:50491", "tcp://10.0.1.165:50492")

def ping_tx():
    while run:
        ping_esttc.tx(ping_msg)
        pings += 1
        time.sleep(ping_delay)

def ping_rx():
    while run:
        try:
            rx = ping_esttc.rx(zmq.NOBLOCK)
            if rx == pong_msg:
                print("------ pong received!")
                ping_pongs += 1
            elif rx == ping_msg:
                print("ping back")
            else:
                print("------ weird pong: ", rx)
        except zmq.ZMQError:
            continue

def pong():
    while run:
        try:
            rx = pong_esttc.rx(zmq.NOBLOCK)
            if rx == ping_msg:
                print("--- ping received!")
                pong_esttc.tx(pong_msg)
                pongs += 1
            elif rx == pong_msg:
                print("--- pong back")
            else:
                print("--- weird ping: ", rx)
        except zmq.ZMQError:
            continue

if __name__ == '__main__':
    t_pong = Thread(target=pong)
    t_ping_rx = Thread(target=ping_rx)
    t_ping_tx = Thread(target=ping_tx)

    t_pong.start()
    t_ping_rx.start()
    t_ping_tx.start()

    input("Press Enter to quit...")
    run = False

    t_pong.join()
    t_ping_rx.join()
    t_ping_tx.join()

    ping_loss = "{.2f} %".format((pings-pongs)/pings*100) if pings != 0 else 'N/A'
    pong_loss = "{.2f} %".format((pongs-ping_pongs)/pongs*100) if pongs != 0 else 'N/A'
    total_loss = "{.2f} %".format((pings-ping_pongs)/pings*100) if pings != 0 else 'N/A'

    print('Statistics:')
    print('  pings:      ', pings)
    print('  pongs:      ', pongs)
    print('  ping pongs: ', ping_pongs)
    print('  ping loss:  ', ping_loss)
    print('  pong loss:  ', pong_loss)
    print('  total loss: ', total_loss)
    