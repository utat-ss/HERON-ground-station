import time

from esttc_interface import ESTTCWrapper

esttc = ESTTCWrapper("localhost")

txpacket = None

if __name__ == "__main__":
    while True:
        rx = esttc.rx()
        if "ACK" in rx:
            continue
        else:
            print(rx)
            txpacket = rx + " ACK"
            esttc.tx("ACK")
