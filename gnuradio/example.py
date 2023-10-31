from esttc_interface import esttc_rx, esttc_tx
import time
import zmq

if __name__ == '__main__':

    try:
        while True:
            esttc_tx([4,3,2,1,5])
            time.sleep(1000)
            try:
                print(esttc_rx())
            except zmq.error.Again:
                print('timeout')
    except KeyboardInterrupt:
        print("\nExit\n")
