import sys
import transceivers
import signal
import sys
import rpyc
import systemd.daemon
import multiprocessing as mp
import gc
import os
import subprocess

class GSServer(rpyc.Service):

    def on_disconnect(self, conn):
        if hasattr(self, 'trx') and self.trx != None:
            self.trx.terminate()
            self.trx.wait()
            delattr(self, 'trx')
            gc.collect()

    def exposed_start_trx(self, name: str):
        
        # I have tried a lot of different things...
        # Nothings beats brute force calling python3 from command line

        # trx_inst = importlib.import_module("transceivers."+name)
        # self.trx = self.ctx.Process(target=trx_inst.main)
        
        # trx_inst = getattr(importlib.import_module("transceivers."+name), name)
        # self.trx = trx_inst()
        
        # self.trx = mp.Process(target=os.system, args=("python3 "+name+".py",))
        
        # self.trx.start()
        
        self.trx = subprocess.Popen(["python3", name+".py"])

def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__))+"/transceivers")
    systemd.daemon.notify("READY=1")
    serv = rpyc.ThreadedServer(GSServer(), port=50600)

    def handler(sig=None, frame=None):
        systemd.daemon.notify("STOPPING=1")
        sys.exit(0)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    serv.start()


if __name__ == '__main__':
    main()

