import time
from threading import Thread
import signal
import zmq
import argparse
from xmlrpc.client import ServerProxy
import ax25
import stations
import satellite
from predict import PredictWrapper

ping_delay = 3
ping_msg = ax25.str2pkt('=4339.60N/07923.85W-Hello from the University of Toronto Aerospace Team', 'CQ', 'VE3SGH', 'OK0BDT-1')
norad = 55098
freq = 436_025_000
outfile_prefix = f"/home/heron/recordings/other_satellites/BDSAT-2"
mode = 3 # AX.25 G3RUH
dpler = ServerProxy(f"http://10.0.7.91:50600")
hang_time = 2

max_rotator_attemps = 10
run_program = True

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
        with open(digi_outfile, "w") as outfile:
            while self._run or recv_flush>0:
                try:
                    resp = txer.rx_bytes(zmq.NOBLOCK)
                    try:
                        ax25msg = ax25.pkt2str(resp)
                        outfile.write(ax25msg + "\n")
                    except:
                        outfile.write("".join(chr(c) for c in resp))
                except zmq.ZMQError:
                    pass
                recv_flush -= 1-self._run

    def pinger(self, txer):
        while self._run:
            txer.tx_bytes(ping_msg)
            time.sleep(ping_delay)

    def start(self):
        (self.client, self.channel, self.flow, self.digi, self.rot) = stations.setup_herongs(rot_config=int(norad), tx_config=int(80))

        for i in range(max_rotator_attemps):
            try:
                print(self.rot.get_tracking_status())
                break
            except:
                if i+1 == max_rotator_attemps: raise

        outfile = f"{outfile_prefix}-38k4-{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}"

        self.flow.set_cfo(freq + 100_000)
        self.flow.set_freq(freq)
        self.flow.set_mode(mode)
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
        for i in range(max_rotator_attemps):
            try:
                self.rot.disable_tracking()
                break
            except:
                if i+1 == max_rotator_attemps: raise
        dpler.disable_correction()
        self.t_pinger.join()
        self.t_rx_sink.join()
        self.channel.close()
        self._stopped = True

if __name__ == '__main__':

    p = PredictWrapper("VE3SGH", 43.66, -79.4)
    bdsat = satellite.Satellite(norad, freq, 3)

    def signal_handler(signum, frame):
        global run_program
        print("\nExitting...")
        run_program = False
    signal.signal(signal.SIGINT, signal_handler)

    times, _ = p.get_doppler_shifts(bdsat)
    print("Next pass: ", time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(times[0])))

    e = None

    while run_program:
        if time.time() >= times[-1]:
            if e:
                print("Pass stopping")
                e.stop()
                e = None
            bdsat.update_tle()
            times, _ = p.get_doppler_shifts(bdsat)
            print("Next pass: ", time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(times[0])))
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
    
    print("done")
    