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
import datetime



class RX_Command():
    def __init__(self, outlog_path):
        rx_log = os.scandir(outlog_path)
        if len(rx_log) == 0:
            rx_log_path = outlog_path + "rx_log_" + datetime.now().strftime("%d/%m/%Y") + ".txt"
        elif datetime.now().day == 1:
            rx_log_path = outlog_path + "rx_log_" + datetime.now().strftime("%d/%m/%Y") + ".txt"
        self.outlog = rx_log_path
        self.packed = "../recordings/packets.txt"

    def receive(self):
        ack = False
        while True:
            rx_process = subprocess.Popen(["python3 ../rx/rx_quaddemod.py"])
            if os.path.exists(self.packed) and os.stat(self.packed).st_size != 0:
                with open(self.packed) as packets, open(self.outlog, 'a') as outlog:
                    outlog.write("@ " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    for line in packets:
                        if "ACK" in line:
                            ack = True
                            outlog.write(line)
                            outlog.write('\n')
                rx_process.terminate()
                return ack

                
