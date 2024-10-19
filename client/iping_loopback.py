from threading import Thread
import zmq
import stations

ping_delay = 1
ping_msg = "ES+R2200\r"

pings_sent = 0
pings_rcvd = 0
run = True

def rx_sink(ping_esttc):
    global pings_rcvd
    recv_flush = 100000
    while run or recv_flush>0:
        try:
            msg = ping_esttc.rx(zmq.NOBLOCK)
            if msg == ping_msg:
                pings_rcvd += 1
                print("ping received [{}]".format(pings_rcvd))
        except zmq.ZMQError:
            pass
        recv_flush -= 1-run

def pinger(ping_esttc):
    global pings_sent
    global pings_rcvd
    ping_esttc.set_timeout(ping_delay*1000)
    while run:
        ping_esttc.tx(ping_msg)
        pings_sent += 1
        try:
            msg = ping_esttc.rx()
            if msg == ping_msg:
                pings_rcvd += 1
                print("ping received [{}]".format(pings_rcvd))
        except zmq.ZMQError:
            print('timeout')

if __name__ == '__main__':

    (client, channel, flow, digi, rot) = stations.setup_herongs(rot_config="lab")
    # (client, channel, flow, digi, rot) = stations.setup_pluto(rx_config="partial")

    t_pinger = Thread(target=pinger, args=[digi,])
    t_pinger.start()

    input("Press Enter to quit...\n")
    run = False

    t_pinger.join()
    rx_sink(digi)

    total_loss = "{0:.2f} %".format((pings_sent-pings_rcvd)/pings_sent*100) if pings_sent != 0 else 'N/A'

    print('Statistics:')
    print('  pings sent:      ', pings_sent)
    print('  pongs received:  ', pings_rcvd)
    print('  total loss:      ', total_loss)
    