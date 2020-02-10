# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                      										#
# Purpose: Provide an interface for running the OBC <--> Comms Tx/Rx Link	#
# Author: Gabe Sher pls hit me up on slack @Gabe if there's an issue		#
# Date: 2020-02-07                                							#
#									                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from packet_creation import crc
from packet_creation import make_message as m
import os
import subprocess
import time

if __name__ == "__main__":
    FAIL='\033[91m'
    WARNING='\033[93m'
    GREEN='\033[92m'
    ENDC='\033[0m'
    BOLD='\033[1m'
    # Make directory with current date
    # Logging isn't working so well so it's been removed for now
    #logdir = "test"+time.strftime("%F-%H-%M-%S")
    #os.system("mkdir " + logdir)
    outpath = "cmdout.bin"

    # Set up 0 packet -- will be used a lot
    zero_packet = m.es_frame_text("0")

    # Create prompt and operate
    packetcount = 0

    while (True):
        print ("\nType one of the following commands OR type an opcode in two characters (e.g. 02 or 11)")
        print ("==============")
        print ("PIPE :: Enter PIPE mode (if you haven't already done it)")
        print ("BCN OFF :: Turn the beacon off")
        print ("BCN ON :: Turn the beacon on")
        print ("GET FREQ :: Get current centre frequency")
        print ("SET FREQ :: Set current centre frequency")
        
        cmd =  input("\nPlease enter your command:\t").upper().strip()
    
        if (cmd == "PIPE" or cmd=="BCN OFF" or cmd=="BCN ON" or cmd=="GET FREQ"):
            os.system("cp messages/ESTTC/ES_" + cmd.replace(' ', '_') + ".bin " + outpath)
            os.system("python2 tx/gfsk_tx.py")
            continue

        if (cmd == "SET FREQ"):
            print("Please run the program EnduroSat provides for calculation of the 8-nybble notation of the frequency.")
            print("Please enter the output for your desired frequency, as text:")
            print("e.g. for 435 MHz, you'd enter \"76620F41\"")
            freq = input("\t")
            packet = m.es_frame_text("ES+W2201"+freq.strip()+"\x0d")
            packet += zero_packet*2

            # Write to files for sending and logging
            m.write_to_file(outpath, packet)
            os.system("python2 tx/gfsk_tx.py")
            continue
        
        # Create actual message packet
        # FORMAT:
        ## Bytes 0-1 ---- Command ID
        ## Byte 2 ------- Opcode
        ## Bytes 3-6 ---- Argument 1
        ## Bytes 7-10 --- Argument 2
        ## Bytes 11-14 -- Password
        try:
            assert(len(cmd) == 2)
        except AssertionError:
            print(FAIL+BOLD+"ERROR: "+WARNING+"You have to write the opcode in two characters, like 02 or 11. Not 2 or 0x02."+ENDC)
            continue

        print("Please input the " +GREEN+"command ID"+ENDC+ " you'd like to use (1 to 65535):")
        cmdid = input("\t")

        print("Please input the " +GREEN+"first argument"+ENDC+ " in HEX format:")
        print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. *Please use spaces*.)")
        arg1 = input("\t")
        
        print("Please input the " +GREEN+"second argument"+ENDC+ " in HEX format:")
        arg2 = input("\t")
        
        print("Please input the " +GREEN+"password"+ENDC+ " in HEX format:")
        pwd = input("\t")
        
        message = cmdid.strip() + " " + cmd + " " +  arg1.strip() + " " + arg2.strip() + " " + pwd.strip()
        """# Start message off with op-code
        message = cmd + " "
        
        zero_args = ["00", "01", "13", "21", "24", "30", "32", "37"]
        one_arg   = ["03", "04", "05", "06", "14", "36", "42"]
        two_args = ["02", "10", "11", "12", "15", "20", "22", "23", "31", "33", "34", "35", "40", "41"]
        if (cmd in zero_args):
            # Zero arguments -- simple

            # Create message
            message += "00 "*8   # Arguments 1 and 2 -- irrelevant

        elif (cmd in one_arg): 
            # One argument -- a bit less simple
            
            # Get argument
            print("Please input the argument in HEX format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. *Please use spaces*.)")
            arg1 = input("\t")

            # Create message
            message += arg1.strip() + " " 
            message += "00 "*4   # Argument 2 is just empty
        
        elif (cmd in two_args):
            # Two arguments

            # Get argument 1
            print("Please input the FIRST argument in HEX format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. Spaces are optional)")
            arg1 = input("\t")

            # Get argument 2
            print("Please input the SECOND argument in HEX format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. Spaces are optional)")
            arg2 = input("\t")

            # Create message
            message += arg1.strip() + " "
            message += arg2.strip() + " "
        else:
            print("Something went wrong, I wasn't expecting that command number.")
            print("Please try again. Make sure to select something from the list, like \"00\" or \"12\"")
            continue
        """
        # Turn into packet, pad with 2 "0" packets for safe transmission
        #message += "55 54 41 54"
        print("Sending:", message)
        message_string_array = message.split()
        message_array = [int(byte, 16) for byte in message_string_array]
        encoded_message = m.encode_message(message_array)
        packet = m.es_frame_bytes(encoded_message)
        packet += zero_packet*2

        # Write to files for sending and logging
        #m.write_to_file("./"+logdir+"/packet"+str(packetcount)+".bin", packet) # Commented out because not working, oddly
        #os.system("echo 'Sent packet for command " + cmd + ", looked like:' >> " + logdir + "/log.txt")
        #os.system("echo '" + str(packet) + "' >> " + logdir + "/log.txt")
        #os.system("echo '' >> " + logdir + " /log.txt")
        m.write_to_file(outpath, packet)
        packetcount += 1

        os.system("python2 tx/gfsk_tx.py")
