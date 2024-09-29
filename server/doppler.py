import subprocess
import time
import re
from xmlrpc.server import SimpleXMLRPCServer
import socket
import requests
import tempfile
from threading import Thread
import signal
import systemd.daemon

# THIS IS BAD, please change to rest api or rpyc

class DopplerServer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.tle_file = tempfile.NamedTemporaryFile("w+", suffix=".tle", delete_on_close=False)
        self.tle_file.close()
        self.name = "ISS (ZARYA)"
        self.norad = 25544
        self.freq = 437_800_000
        self._times = []
        self._shifts = []
        self.trx_addr = ('localhost', 52002)
        self._enable_doppler = False
        self._run_loop = True
        self.hang_time = 2

    def __del__(self):
        self.tle_file.close()

    def set_freq(self, freq):
        self.freq = freq
    
    def enable_correction(self):
        self._enable_doppler = True
        self._load_next_pass()
    
    def disable_correction(self):
        self._enable_doppler = False
    
    def stop(self):
        self._run_loop = False
    
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
        if "No GP data found" in resp:
            raise LookupError("norad does not exist")
        self.name = resp.splitlines()[0].strip()
        with open(self.tle_file.name, mode='w+') as f:
            f.write(resp)
    
    def _load_next_pass(self):
        try:
            output = subprocess\
                .check_output(["predict", "-t", self.tle_file.name, "-dp", self.name])\
                .decode()\
                .splitlines()
            line_pattern = re.compile(r"(\d*),.*,(-?\d*\.?\d*)")
            self._times = []
            self._shifts = []
            for line in output:
                m = line_pattern.match(line)
                self._times.append(int(m.group(1)))
                self._shifts.append(float(m.group(2)))
        except Exception as e:
            print(e)

    def _execute_pass(self):
        """Blocking function that exits on pass completeion. Returns True if error ocurred"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                client.connect(self.trx_addr)
                i = 0
                curr = int(time.time())
                while i < len(self._times) and curr > self._times[i]:
                    i += 1
                print("staring pass: " + self.name)
                while i < len(self._times) and self._enable_doppler and self._run_loop:
                    curr = int(time.time())
                    if(self._times[i] > curr):
                        time.sleep(self._times[i]-curr)
                    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.times[i])))
                    client.sendall(f"F  {int(self.freq*(1+self._shifts[i]/100e6))}\n".encode("ASCII"))
                    if(client.recv(1024).decode("UTF-8").strip() != "RPRT 0"):
                        print("bad response")
                        break
                    client.sendall("f\n".encode("ASCII"))
                    print(client.recv(1024).decode("UTF-8").strip())
                    client.sendall(f"I  {int(self.freq*(1-self._shifts[i]/100e6))}\n".encode("ASCII"))
                    if(client.recv(1024).decode("UTF-8").strip() != "RPRT 0"):
                        print("bad response")
                        break
                    client.sendall("i\n".encode("ASCII"))
                    print(client.recv(1024).decode("UTF-8").strip())
                    i+=1
                client.sendall('q\n'.encode("ASCII"))
                print("finished pass: " + self.name)
        except OSError as e:
            print(e)
            return True
        return False

    def run(self):
        pass_error = False
        while(self._run_loop):
            if not self._enable_doppler:
                time.sleep(self.hang_time)
            elif len(self._times) > 0:
                if time.time() >= self._times[-1]:
                    self._load_next_pass()
                elif time.time() >= self._times[0]-self.hang_time and not pass_error:
                    pass_error = self._execute_pass()
                else:
                    time.sleep(self.hang_time)
                    pass_error = False

def main():
    server = SimpleXMLRPCServer(("0.0.0.0", 50600), allow_none=True)
    inst = DopplerServer()
    server.register_instance(inst)
    t = Thread(target=server.serve_forever)
    t.start()
    inst.start()
    systemd.daemon.notify("READY=1")

    def handler(sig=None, frame=None):
        inst.stop()
        systemd.daemon.notify("STOPPING=1")
        
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    inst.join()
    server.shutdown()
    t.join()

if __name__ == "__main__":
    main()