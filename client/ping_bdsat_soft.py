from threading import Thread
import zmq
import ax25
import stations

ping_delay = 3
ping_msg = ax25.str2pkt('Hello from UTAT :)', 'CQ', 'VE3SGH', 'OK0BDT')
norad = 55098
freq = 436_025_000

class ExecutePass():

    def rx_sink(self, txer):
        global resps_rcvd
        recv_flush = 100000
        while self.run or recv_flush>0:
            try:
                resp = txer.rx_bytes(zmq.NOBLOCK)

                try: print(ax25.pkt2str(resp))
                except: print([chr(c) for c in resp])
            except zmq.ZMQError:
                pass
            recv_flush -= 1-self.run

    def start(self):
        (self.client, self.channel, self.flow, self.digi, self.rot) = stations.setup_herongs()

        self.flow.set_mode(3)
        
        self.run = True
        self.t_rx_sink = Thread(target=self.rx_sink, args=[self.digi,])
        self.t_rx_sink.start()
    
    def stop(self):
        self.run = False
        self.t_rx_sink.join()
        self.channel.close()

if __name__ == '__main__':

    e = ExecutePass()
    e.start()

    input("Press Enter to quit...\n")

    e.stop()
    