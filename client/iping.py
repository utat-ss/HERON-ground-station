import time
from threading import Thread
import zmq
from xmlrpc.client import ServerProxy
import rpyc
from esttc_interface import ESTTCWrapper

ping_delay = 5
ping_msg = "ES+R2200\r"
freq = 435_100_000
az = 38
el = 5
gsflow = ServerProxy("http://10.0.7.91:8080")
plflow = ServerProxy("http://10.0.1.165:8080")
rxer = ESTTCWrapper("tcp://10.0.7.91:50491", "tcp://10.0.7.91:50492")
txer = ESTTCWrapper("tcp://10.0.1.165:50491", "tcp://10.0.1.165:50492")
rot = rpyc.connect("10.0.7.91", 18866).root.K3NG

pings_sent = 0
pings_rcvd = 0
run = True

def txer_rx_sink():
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            txer.rx(zmq.NOBLOCK)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def rxer_rx_sink():
    global pings_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            msg = rxer.rx(zmq.NOBLOCK)
            if msg == ping_msg:
                pings_rcvd += 1
                print("ping received [{}]".format(pings_rcvd))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger():
    global pings_sent
    global pings_rcvd
    rxer.set_timeout(ping_delay*1000)
    while run:
        txer.tx(ping_msg)
        pings_sent += 1
        try:
            msg = rxer.rx()
            if msg == ping_msg:
                pings_rcvd += 1
                print("ping received [{}]".format(pings_rcvd))
        except zmq.ZMQError:
            print('timeout')

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


    t_txer_rx_sink = Thread(target=txer_rx_sink)
    t_pinger = Thread(target=pinger)

    t_txer_rx_sink.start()
    t_pinger.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    rxer_rx_sink()
    t_txer_rx_sink.join()

    total_loss = "{0:.2f} %".format((pings_sent-pings_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', pings_rcvd)
    print('  total loss:      ', total_loss)
    
