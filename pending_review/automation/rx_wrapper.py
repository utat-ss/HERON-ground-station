"""
rx_wrapper.py

This function is meant to take in the packaged RX information from the RX flowgraph
and interpret it to check for ACKs and read data.

Author(s): Adyn Miles
"""

'''
TODO :

- Get legible information from the HERON RX BB code.
- Use a sample satellite RX code to start interpreting information from the satellite.
- ACK function that returns true if the response contains an ACK
- Function for reading the data section of the incoming packet, and logging it to rx_log_path
'''

import subprocess
import os
from datetime import datetime
import constants as const



class RX_Command():
    def __init__(self, outpath, outlog_path):
        rx_log = os.scandir(outlog_path)
        rx_log_path = outlog_path + "rx_log_" + datetime.now().strftime("%d-%m-%Y") + ".txt"
        self.outlog = rx_log_path
        self.outpath = outpath
        # self.packed = "../recordings/packets.txt" <-- temp change for testing purposes, reinstate when ready
        self.packed = "commands/test_ack.bin"

    def receive(self):
        ack = False
        while True:
            # rx_process = subprocess.Popen(["python3 ../rx/rx_quaddemod.py"])
            if os.path.exists(self.packed) and os.stat(self.packed).st_size != 0:
                with open(self.packed, "rb") as packets, open(self.outlog, 'a') as outlog:
                    outlog.write("@ " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    for line in packets:
                        if const.ACK in line:
                            ack = True
                            outlog.write("ACK")
                            outlog.write('\n')
                        elif const.NACK in line:
                            outlog.write("NACK")
                            outlog.write("\n")
                # rx_process.terminate()
                return ack

                
