from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ip = "10.0.1.165"
esttc = ESTTCWrapper(f"tcp://{ip}:50491", f"tcp://{ip}:50492")
run = True

def listen():
    line = 0
    while run:
        try:
            msg = esttc.rx(zmq.NOBLOCK)
            line += 1
            print('[{}] {}'.format(line, msg))
        except zmq.ZMQError:
            pass
    
if __name__ == '__main__':
    t = Thread(target=listen)
    t.start()
    input("Press Enter to quit...\n")
    run = False
    t.join()
