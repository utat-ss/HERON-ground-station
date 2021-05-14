# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                           #
# Purpose: CLI interface for full two-way comms between the GS and the sat  #
# Author: Gabe Sher                                                         #
# Last updated: 2020-10-06                                                  #
#                                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from packet_creation import crc
from packet_creation import make_message as m
import os
import subprocess
import time
from interface.commands import commands as op

# def check_arg(args, opcode):
#     if (args == [0,0]):
#         return (True, None)
#     else:
#         return (False, "Not [0,0]")

if __name__ == "__main__":
    FAIL='\033[91m'
    WARN='\033[93m'
    GRN ='\033[92m'
    ENDC='\033[0m'
    BOLD='\033[1m'

    # FEATURES
    #   * simulates simple TX control loop:
    #       * prompts user for a command
    #       * assigns a sequence number ("command ID") to new command
    #       * turns command message into a packet
    #       * writes packet to a .bin
    #       * calls TX flowgraph, which transmits that packet
    #       * allows you to either retransmit or move to next packet
    #   * commands available:
    #       * UTAT Commands (SS-HERON-008):
    #           * see commands.json for progress
    #       * ESTTC commands:
    #           * PIPE to enter PIPE mode
    #           * PIPE_TIMEOUT to set PIPE mode timeout TODO
    #           * BCN_ON, BCN_OFF
    #           * GET_FREQ, SET_FREQ
    #   * logs TX'd commands to a DB TODO

    outpath = "cmdout.bin"
    
    # Create '0' packet - for padding
    zero_packet = m.es_frame_text("0")

    valid_esttc_cmds = ["PIPE", "BCN_ON", "BCN_OFF", "GET_FREQ"]
    # Simple TX Loop
    seqno = 0
    while (True):
        print(BOLD+"Type a valid op-code in HEX."+ENDC+" Acceptable formats: 06, 0x02, 10, 0x21")
        print(BOLD+"OR, type one of the following ESTTC commands:"+ENDC, valid_esttc_cmds)

        cmd = input(GRN+BOLD+" >>> "+ENDC).upper().strip()

        # If sending an ESTTC command, simply copy in the message of interest
        if (cmd in valid_esttc_cmds):
            os.system("cp messages/ESTTC/ES_" + cmd + ".bin " + outpath)
            os.system("xxd " + outpath)
            os.system("python3 tx/gfsk_tx.py")
            print("ESTTC command sent. Looping...")
            # TODO might have to have different functionality for PIPE_TIMEOUT and SET_FREQ (arguments)
            continue

        # If don't have a valid command, report as such
        if (len(cmd) > 2 and cmd[0:2] == "0X"):
            cmd = cmd[2:]
        if (not (len(cmd) == 2 and cmd[0] in "01234" and cmd[1] in "01234567")):
            print(FAIL+"That doesn't seem to be a valid command. Please try again..."+ENDC)
            continue

        # If we make it here, we have a valid command to send
        # Collect & validate arguments
        args = []
        print ("You have selected: " + (op[cmd])["name"]+ENDC)
        for i in range(op[cmd]["args"]):
            print("Please input argument", i, ":")
            arg_in = input(GRN+BOLD+" >>> "+ENDC)
            args.append(arg_in)
        while (len(args) < 2):
            args.append(0)
        
        # (arg_check, arg_err) = check_arg(args, cmd)
        # if (not arg_check):
        #     print ("Arguments input incorrectly. Got error message:")
        #     print("::"+FAIL, arg_err)
        #     print(WARN+"Please try again..."+ENDC)
        #     continue
        # Convert arguments to useful format
        # TODO - currently, assuming we'll only use ARG-LESS commands

        # Now have: Command ID (Seq No.), OpCode, 0-2 valid Arguments, and a Password
        # Can assemble a packet.

        # Hacky but: this assembles numbers as an array of 1-byte values.

        # First: the Command ID
        msg_array = [(seqno & 0xFF00) >> 8, seqno & 0xFF]
        
        # Next: add in the OpCode, which was collected as a HEX value
        msg_array.append(int(cmd, 16))

        # Next: add in the arguments:
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

        # Next: Add in the password
        msg_array.append(0x55)
        msg_array.append(0x54)
        msg_array.append(0x41)
        msg_array.append(0x54) # TODO : replace with actual password

        # Should now have assembled the full decoded packet. 

        # Encode in UTAT format, wrap in ES frame.
        enc_msg = m.encode_message(msg_array) # comes out as bytes
        packet = m.es_frame_bytes(enc_msg) # input and output as bytes

        # Extend with "0" packets, since that seems necessary. 
        # TODO test without this and possibly remove.
        packet += zero_packet

        m.write_to_file(outpath, packet)
        
        # Send, block and wait for user to move forward or repeat
        while (True):
            print(BOLD+"Sending the following message. Observe on RX to see what's received."+ENDC)
            print([hex(byte) for byte in msg_array])
            os.system("python3 tx/gfsk_tx.py")
            
            print("")
            print("Would you like to resend ('r') or move to the next command ('n')?")
            action = input(GRN+BOLD+" >>> "+ENDC)

            while (action not in 'rn'):
                print(FAIL+"Invalid input."+ENDC+" Would you like to resend ('r') or move to the next command ('n')?")
                action = input(GRN+BOLD+" >>> "+ENDC)
            if (action == 'r'):
                action = 'x'
                continue
            elif (action == 'n'):
                action = 'x'
                break
        print("\n=====================\n")

        # Sequence number handling
        seqno = seqno + 1
        if (seqno > 0xFFFF):
            seqno = 0

