from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

esttc = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
run = True

def listen():
    while run:
        try:
            print(esttc.rx(zmq.NOBLOCK))
        except zmq.ZMQError:
            pass
    
if __name__ == '__main__':
    t = Thread(target=listen)
    t.start()
    input("Press Enter to quit...\n")
    run = False
    t.join()
