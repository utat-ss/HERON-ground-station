import subprocess
import time
import re
from xmlrpc.server import SimpleXMLRPCServer
import socket
import requests
import tempfile
from threading import Thread
import signal
import sys

class DopplerServer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.tle_file = tempfile.NamedTemporaryFile('w+', delete_on_close=False)
        self.tle_file.close()
        self.name = None
        self.norad = 0
        self.freq = 100
        self.times = []
        self.shifts = []
        self.trx_addr = ('10.0.7.91', 52002)
        self.enable_doppler = False
        self.run_loop = True

    def __del__(self):
        self.tle_file.close()

    def set_freq(self, freq):
        self.freq = freq
    
    def enable_correction(self):
        self.enable_doppler = True
        self.load_next_pass()
    
    def disable_correction(self):
        self.enable_doppler = False
    
    def stop(self):
        self.run_loop = False
    
    def load_norad(self, norad: int):
        self.norad = norad
        self.reload_norad()
    
    def reload_norad(self):
        resp = requests.get(
            "https://celestrak.org/NORAD/elements/gp.php",
            params={"CATNR":str(self.norad)},
            timeout=5
        ).text
        print(resp)
        self.name = resp.splitlines()[0].strip()
        with open(self.tle_file.name, mode='w+') as f:
            f.write(resp)
    
    def load_next_pass(self):
        output = subprocess\
            .check_output(["predict", "-t", self.tle_file.name, "-dp", self.name])\
            .decode()\
            .splitlines()
        line_pattern = re.compile(r"(\d*),.*,(-?\d*\.?\d*)")
        self.times = []
        self.shifts = []
        for line in output:
            m = line_pattern.match(line)
            self.times.append(int(m.group(1)))
            self.shifts.append(float(m.group(2)))

    def execute_pass(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect(self.trx_addr)
            i = 0
            curr = int(time.time())
            while i < len(self.times) and curr > self.times[i]:
                i += 1
            while i < len(self.times) and self.enable_doppler and self.run_loop:
                curr = int(time.time())
                if(self.times[i] > curr):
                    time.sleep(self.times[i]-curr)
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.times[i])))
                client.sendall(f"F  {int(self.freq*(1+self.shifts[i]/100e6))}\n".encode("ASCII"))
                if(client.recv(1024).decode('UTF-8').strip() != "RPRT 0"):
                    print("bad response")
                    break
                client.sendall("f\n".encode("ASCII"))
                print(client.recv(1024).decode('UTF-8').strip())
                client.sendall(f"I  {int(self.freq*(1-self.shifts[i]/100e6))}\n".encode("ASCII"))
                if(client.recv(1024).decode('UTF-8').strip() != "RPRT 0"):
                    print("bad response")
                    break
                client.sendall("i\n".encode("ASCII"))
                print(client.recv(1024).decode('UTF-8').strip())
                i+=1
            client.sendall('q\n'.encode("ASCII"))

    def run(self):
        while(self.run_loop):
            if not self.enable_doppler:
                time.sleep(1)
            elif len(self.times) > 0:
                if time.time() >= self.times[-1]:
                    self.load_next_pass()
                elif time.time() >= self.times[0] - 1:
                    self.execute_pass()
                else:
                    time.sleep(1)

def main():
    server = SimpleXMLRPCServer(("0.0.0.0", 50600), allow_none=True)
    inst = DopplerServer()
    server.register_instance(inst)
    t = Thread(target=server.serve_forever)
    t.start()
    inst.start()

    def handler(sig=None, frame=None):
        inst.stop()
        
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    inst.join()
    server.shutdown()
    t.join()

if __name__ == "__main__":
    main()