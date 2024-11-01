import time
from threading import Thread
import zmq
from xmlrpc.client import ServerProxy
import datetime
from . import ax25
from . import stations
from . import satellite
from .predict import PredictWrapper

ping_delay = 3
ping_msg = ax25.str2pkt('=4339.60N/07923.85W-Hello from the University of Toronto Aerospace Team', 'CQ', 'VE3SGH', 'OK0BDT-1')
norad = 55098
freq = 436_025_000
dpler = ServerProxy(f"http://10.0.7.91:50600")
hang_time = 2

run_program = True

def exit_on_keypress():
    global run_program
    input("Press Enter to quit...\n")
    run_program = False

class ExecutePass():

    def __init__(self):
        self._run = False
        self._stopped = True

    def __del__(self):
        if not self._stopped and self._run:
            self.stop()

    def rx_sink(self, txer, digi_outfile):
        global resps_rcvd
        recv_flush = 100000
        with open(digi_outfile, "w+") as outfile:
            while self._run or recv_flush>0:
                try:
                    resp = txer.rx_bytes(zmq.NOBLOCK)
                    outfile.write(ax25.pkt2str(resp) + "\n")
                except zmq.ZMQError:
                    pass
                recv_flush -= 1-self._run

    def pinger(self, txer):
        while self._run:
            txer.tx_bytes(ping_msg)
            time.sleep(ping_delay)

    def start(self):
        (self.client, self.channel, self.flow, self.digi, self.rot) = stations.setup_herongs(rot_config=int(norad), tx_config=int(80))

        print(self.rot.get_tracking_status())

        outfile = f"~/recordings/other_satellites/BDSAT-2-48k-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}"

        self.flow.set_cfo(freq + 100_000)
        self.flow.set_freq(freq)
        self.flow.set_mode(3)
        self.flow.set_output(outfile + ".fc32")

        dpler.load_norad(norad)
        dpler.set_freq(freq)
        dpler.enable_correction()
        
        self._run = True
        self._stopped = False
        self.t_pinger = Thread(target=self.pinger, args=[self.digi,])
        self.t_rx_sink = Thread(target=self.rx_sink, args=[self.digi, outfile+".txt"])
        self.t_pinger.start()
        self.t_rx_sink.start()
    
    def stop(self):
        self._run = False
        self.rot.disable_tracking()
        dpler.disable_correction()
        self.t_pinger.join()
        self.t_rx_sink.join()
        self.channel.close()
        self._stopped = True

if __name__ == '__main__':

    p = PredictWrapper("VE3SGH", 43.66, -79.4)
    bdsat = satellite.Satellite(norad, freq, 3)

    t = Thread(target=exit_on_keypress)
    times, _ = bdsat.get_doppler_shifts()
    print("Next pass: ", +datetime.strftime("%Y-%m-%d-%H-%M-%S", datetime.localtime(times[0])))

    e = None

    while run_program:
        if time.time() >= times[-1]:
            if e:
                print("Pass stopping")
                e.stop()
                e = None
            bdsat.update_tle()
            times, _ = bdsat.get_doppler_shifts()
            print("Next pass: ", +datetime.strftime("%Y-%m-%d-%H-%M-%S", datetime.localtime(times[0])))
        elif time.time() >= times[0]-hang_time and not e:
            print("Pass starting!")
            e = ExecutePass()
            e.start()
        else:
            time.sleep(hang_time)
    
    if e:
        print("Pass stopping")
        e.stop()
        e = None
        
    t.join()

    # e = ExecutePass()
    # e.start()

    # input("Press Enter to quit...\n")

    # e.stop()
    