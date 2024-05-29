"""
tx_wrapper.py

This function essentially works the same as tx_for_bidirectional, except it 
interfaces with the automate.py script rather than with the command line
interface. Sends a command to the TX flowgraph.

Author(s): Adyn Miles
"""

'''
TODO :

    - Add argument checking
    - Add password checking
    - [DONE] Potentially speed up workflow such that every tx.command() call automatically does the PIPE command.
'''

from packet_creation import crc
from packet_creation import make_message as m
import os 
import subprocess
import time
from datetime import datetime
from interface.commands import commands as op
from packet_creation.SHA256 import SHA256HASH as hash
import constants as const

test_bin_file = "commands/test_ack.bin"

class TX_Command():
    def __init__(self, outpath, outlog_path):
        tx_log = os.scandir(outlog_path)
        tx_log_path = outlog_path + "tx_log_" + datetime.now().strftime("%d-%m-%Y") + ".txt"
        self.outpath = outpath
        self.outlog = tx_log_path

        self.zero_packet = m.es_frame_text("0")

        self.valid_esttc_cmds = ["PIPE", "GET_FREQ"]

    def command(self, cmd, args=False, pwd=False):
        try:
            seqno = 0
            cmd = cmd.upper().strip()

            os.system("cp ../messages/ESTTC/ES_" + "PIPE" + ".bin " + self.outpath)
            os.system("xxd " + self.outpath)
            os.system("python3 ../tx/gfsk_tx.py")
            print("PIPE command sent. Looping...")
                
                
            if cmd in self.valid_esttc_cmds and cmd != "PIPE":
                os.system("cp ../messages/ESTTC/ES_" + cmd + ".bin " + self.outpath)
                os.system("xxd " + self.outpath)
                os.system("python ../tx/gfsk_tx.py")
                print("ESTTC command sent. Looping...")


            if (len(cmd) > 2 and cmd[0:2] == "0X"):
                cmd = cmd[2:]
            if (not (len(cmd) == 2 and cmd[0] in "01234" and cmd[1] in "01234567")):
                raise ValueError('%s is not a valid command. Sending email to ss-operations email chain') 

            args = []
            file = open(self.outlog, 'a+')
            ranCommand = "\t"
            print ("Sending: " + (op[cmd])["name"])

            file.write("@ " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            file.write(" " + (op[cmd])["name"] +" - Opcode: " + "0x" + cmd + "\n")
            file.write(ranCommand)
            if (len(ranCommand) > 2):
                file.write("\n")
            file.close()

            msg_array = [(seqno & 0xFF00) >> 8, seqno & 0xFF]
            msg_array.append(int(cmd, 16))

            if args == False: 
                args.append(0)

            for arg in args:
                if type(arg) == str:
                    arg = int(arg, 16)
                    msg_array.append((arg & 0xFF000000) >> 24)
                    msg_array.append((arg & 0x00FF0000) >> 16)
                    msg_array.append((arg & 0x0000FF00) >> 8)
                    msg_array.append( arg & 0x000000FF)
                else:
                    msg_array.append((arg & 0xFF000000) >> 24)
                    msg_array.append((arg & 0x00FF0000) >> 16)
                    msg_array.append((arg & 0x0000FF00) >> 8)
                    msg_array.append( arg & 0x000000FF)

            if pwd != False:
                msg_array.append(0x55)
                msg_array.append(0x54)
                msg_array.append(0x41)
                msg_array.append(0x54)
                
            enc_msg = m.encode_message(msg_array)
            packet = m.es_frame_bytes(enc_msg)

            packet += self.zero_packet

            m.write_to_file(self.outpath, packet)

            print("Sending: ", [hex(byte) for byte in msg_array])
            os.system("python3 ../tx/gfsk_tx.py")

            # Write ACK to binary file
            ack_file = open(test_bin_file, "wb")
            ack_file.write(const.ACK)
            ack_file.close()

            # Sequence number handling 
            seqno = seqno + 1
            if (seqno > 0xFFFF):
                seqno = 0
        except:
            # command failed, NACK to binary file
            nack_file = open(test_bin_file, "wb")
            nack_file.write(const.NACK)
            nack_file.close()


        