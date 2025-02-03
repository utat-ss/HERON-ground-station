from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper
import argparse

run = True

def listen(digi):
    line = 0
    while run:
        try:
            msg = digi.rx(zmq.NOBLOCK)
            line += 1
            print('[{}] {}'.format(line, msg))
        except zmq.ZMQError:
            pass
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='listen',
        description='dump digital interface Rx')
    parser.add_argument(
        '--ip',
        type=str,
        default='localhost',
        help='ip address of running transceiver')
    args = parser.parse_args()

    esttc = ESTTCWrapper(f"tcp://{args.ip}:50491", f"tcp://{args.ip}:50492")
    t = Thread(target=listen, args=[esttc,])
    t.start()
    input("Press Enter to quit...\n")
    run = False
    t.join()
