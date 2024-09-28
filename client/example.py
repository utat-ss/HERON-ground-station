import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ping_delay = 2
ping_msg = "ES+R2200\r"
esttc = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
run = True

def tx_indefinitely():
    while run:
        esttc.tx(ping_msg)
        time.sleep(ping_delay)

def rx_indefinitely():
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            msg = esttc.rx(zmq.NOBLOCK)
            if msg != ping_msg:
                msg = ' '.join(hex(ord(c)) for c in msg)
                print(msg)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

if __name__ == "__main__":
    t_tx = Thread(target=tx_indefinitely)
    t_rx = Thread(target=rx_indefinitely)

    t_tx.start()
    t_rx.start()

    input("Press Enter to quit...\n")
    run = False

    t_tx.join()
    t_rx.join()
