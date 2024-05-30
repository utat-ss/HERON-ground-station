import time
from threading import Thread

from esttc_interface import ESTTCWrapper

keep_running = True
esttc = ESTTCWrapper("tcp://localhost:50491", "tcp://localhost:50492")


def tx_indefinitely():
    while keep_running:
        esttc.tx("ES+R2200")
        time.sleep(1)


if __name__ == "__main__":
    t = Thread(target=tx_indefinitely)
    t.start()

    try:
        while True:
            rxed = esttc.rx()
            if rxed == "ES+R2200":
                print("Loopback")
            else:
                print(rxed)
    except KeyboardInterrupt:
        keep_running = False

    print("Exiting...")
    t.join()
    print("All threads exited!")
