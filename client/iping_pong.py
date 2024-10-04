import time
from threading import Thread
import zmq
from xmlrpc.client import ServerProxy
import rpyc
from esttc_interface import ESTTCWrapper

ping_delay = 5
pong_delay = 0
ping_msg = "ES+R2200\r"
pong_msg = "ACK"
freq = 435_100_000
az = 38
el = 5
gsflow = ServerProxy("http://10.0.7.91:8080")
plflow = ServerProxy("http://10.0.1.165:8080")
rxer = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
txer = ESTTCWrapper("tcp://10.0.1.165:50491", "tcp://10.0.1.165:50492")
rot = rpyc.connect("10.0.7.91", 18866).root.K3NG

pings = 0
pongs = 0
ping_pongs = 0
run = True
ping_esttc = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
pong_esttc = ESTTCWrapper("tcp://10.0.1.165:50491", "tcp://10.0.1.165:50492")

def ping_tx():
    global pings
    while run:
        ping_esttc.tx(ping_msg)
        pings += 1
        time.sleep(ping_delay)

def ping_rx():
    global ping_pongs
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            rx = ping_esttc.rx(zmq.NOBLOCK)
            if rx == pong_msg:
                ping_pongs += 1
                print("------ pong received [{}]".format(ping_pongs))
            elif rx == ping_msg:
                print("ping back")
            else:
                print("------ weird pong")
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pong():
    global pongs
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            rx = pong_esttc.rx(zmq.NOBLOCK)
            if rx == ping_msg:
                pongs += 1
                print("--- ping received [{}]".format(pongs))
                if run:
                    time.sleep(pong_delay)
                    pong_esttc.tx(pong_msg)
            elif rx == pong_msg:
                print("--- pong back")
            else:
                print("--- weird ping")
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

if __name__ == '__main__':

    rot.set_azimuth(az)
    rot.set_elevation(el)

    gsflow.set_freq(freq)
    gsflow.set_cfo(freq+40_000)
    gsflow.set_lna(True)
    gsflow.set_rx_amp(True)
    gsflow.set_rx_vga_gain(62)
    gsflow.set_rx_if_gain(40)
    plflow.set_freq(freq)
    plflow.set_cfo(freq+40_000)
    plflow.set_tx_gain(89.75)
    plflow.set_rx_gain(4)

    t_pong = Thread(target=pong)
    t_ping_rx = Thread(target=ping_rx)
    t_ping_tx = Thread(target=ping_tx)

    t_pong.start()
    t_ping_rx.start()
    t_ping_tx.start()

    input("Press Enter to quit...\n")
    run = False

    t_pong.join()
    t_ping_rx.join()
    t_ping_tx.join()

    ping_loss = "{0:.2f} %".format((pings-pongs)/pings*100) if pings != 0 else 'N/A'
    pong_loss = "{0:.2f} %".format((pongs-ping_pongs)/pongs*100) if pongs != 0 else 'N/A'
    total_loss = "{0:.2f} %".format((pings-ping_pongs)/pings*100) if pings != 0 else 'N/A'

    print('Statistics:')
    print('  pings:      ', pings)
    print('  pongs:      ', pongs)
    print('  ping pongs: ', ping_pongs)
    print('  ping loss:  ', ping_loss)
    print('  pong loss:  ', pong_loss)
    print('  total loss: ', total_loss)
    
