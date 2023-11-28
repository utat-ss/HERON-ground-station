from esttc_interface import esttc_rx, esttc_tx
import time
import zmq
from threading import Thread

keep_running = True

def tx_indefinitely():
    while keep_running:
        esttc_tx("ES+R2200\r")
        time.sleep(1)

if __name__ == '__main__':
    t = Thread(target=tx_indefinitely)
    t.start()

    try:
        while True:
            print(esttc_rx())
    except KeyboardInterrupt:
        keep_running = False

    print("Exitting...\n")
    t.join()
    print("\nExit\n")
