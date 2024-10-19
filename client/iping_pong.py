import time
from threading import Thread
import zmq
import stations

ping_delay = 2
pong_delay = 0
ping_msg = "ES+R2200\r"
pong_msg = "ACK"
freq = 435_100_000

pings = 0
pongs = 0
ping_pongs = 0
run = True

def ping_tx(ping_esttc):
    global pings
    while run:
        ping_esttc.tx(ping_msg)
        pings += 1
        time.sleep(ping_delay)

def ping_rx(ping_esttc):
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

def pong(pong_esttc):
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

    (gs_client, gs_channel, gs_flow, gs_digi, gs_rot) = stations.setup_herongs(rot_config="lab")
    (pl_client, pl_channel, pl_flow, pl_digi, pl_rot) = stations.setup_pluto(rx_config="partial")

    gs_flow.set_freq(freq)
    gs_flow.set_cfo(freq+40_000)
    pl_flow.set_freq(freq)
    pl_flow.set_cfo(freq+40_000)

    pinger_esttc = gs_digi
    ponger_esttc = pl_digi

    t_pong = Thread(target=pong, args=[ponger_esttc,])
    t_ping_rx = Thread(target=ping_rx, args=[pinger_esttc,])
    t_ping_tx = Thread(target=ping_tx, args=[pinger_esttc,])

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
    
