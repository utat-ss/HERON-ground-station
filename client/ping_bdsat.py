import time
from threading import Thread
import zmq
from xmlrpc.client import ServerProxy
import ax25
import stations

ping_delay = 3
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')
norad = 55098
freq = 436_025_000
dpler = ServerProxy(f"http://10.0.7.91:50600")

class ExecutePass():

    def rx_sink(self, txer):
        global resps_rcvd
        recv_flush = 100000
        while self.run or recv_flush>0:
            try:
                resp = txer.rx_bytes(zmq.NOBLOCK)
                print(ax25.pkt2str(resp))
            except zmq.ZMQError:
                pass
            recv_flush -= 1-self.run

    def pinger(self, txer):
        while self.run:
            txer.tx_bytes(ping_msg)
            time.sleep(ping_delay)

    def start(self):
        (self.client, self.channel, self.flow, self.digi, self.rot) = stations.setup_herongs(rot_config=int(norad), tx_config=int(80))

        print(self.rot.get_tracking_status())

        self.flow.set_cfo(freq + 100_000)
        self.flow.set_freq(freq)
        self.flow.set_mode(3)
        self.flow.set_output("/tmp/bdsat.fc32")

        dpler.load_norad(norad)
        dpler.set_freq(freq)
        dpler.enable_correction()
        
        self.run = True
        self.t_pinger = Thread(target=self.pinger, args=[self.digi,])
        self.t_rx_sink = Thread(target=self.rx_sink, args=[self.digi,])
        self.t_pinger.start()
        self.t_rx_sink.start()
    
    def stop(self):
        self.run = False
        self.rot.disable_tracking()
        dpler.disable_correction()
        self.t_pinger.join()
        self.t_rx_sink.join()
        self.channel.close()

if __name__ == '__main__':

    e = ExecutePass()
    e.start()

    input("Press Enter to quit...\n")

    e.stop()
    