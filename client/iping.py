from threading import Thread
import zmq
import stations

ping_delay = 5
ping_msg = "ES+R2200\r"
freq = 435_100_000

pings_sent = 0
pings_rcvd = 0
run = True

def txer_rx_sink(txer):
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            txer.rx(zmq.NOBLOCK)
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def rxer_rx_sink(rxer):
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

def ping(txer, rxer):
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

    (gs_client, gs_channel, gs_flow, gs_digi, gs_rot) = stations.setup_herongs(rot_config="lab")
    (pl_client, pl_channel, pl_flow, pl_digi, pl_rot) = stations.setup_pluto(rx_config="partial")

    gs_flow.set_freq(freq)
    gs_flow.set_cfo(freq+40_000)
    pl_flow.set_freq(freq)
    pl_flow.set_cfo(freq+40_000)

    txer = gs_digi
    rxer = pl_digi

    t_txer_rx_sink = Thread(target=txer_rx_sink, args=[txer,])
    t_ping = Thread(target=ping, args=[txer, rxer])

    t_txer_rx_sink.start()
    t_ping.start()

    input("Press Enter to quit...\n")
    print("Exitting...")
    run = False

    t_ping.join()
    rxer_rx_sink(rxer)
    t_txer_rx_sink.join()

    total_loss = "{0:.2f} %".format((pings_sent-pings_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', pings_rcvd)
    print('  total loss:      ', total_loss)
    
