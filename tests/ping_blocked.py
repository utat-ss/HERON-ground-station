import time
from threading import Thread
import zmq
from esttc_interface import ESTTCWrapper

ping_delay = 0.5
ping_msg = "ES+R2200\r"

pings_sent = 0
run = True
esttc = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")

def ping():
    global pings_sent
    esttc.set_timeout(1000)
    while run:
        esttc.tx(ping_msg)
        pings_sent += 1
        time.sleep(0.1)
        try:
            msg = esttc.rx()
            print('[{}] {}'.format(pings_sent, msg))
        except zmq.ZMQError:
            print('Timeout! Press ENTER...')
            break

if __name__ == '__main__':

    t_ping = Thread(target=ping)
    t_ping.start()

    input("Press ENTER to quit...\n")
    run = False

    t_ping.join()

    print('Number of successful consecutive packets: ', pings_sent-1)
    