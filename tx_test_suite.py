# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                       										#
# Purpose: Provide an interface for running the OBC <--> Comms Tx/Rx Link	#
# Author: Gabe Sher pls hit me up on slack @Gabe if there's an issue		#
# Date: Thursday, October 31st                      							#
#										                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from packet_creation import crc
from packet_creation import make_message as m
import os
import subprocess
import time

if __name__ == "__main__":
    # Make directory with current date
    # Logging isn't working so well so it's been removed for now
    #logdir = "test"+time.strftime("%F-%H-%M-%S")
    #os.system("mkdir " + logdir)
    outpath = "cmdout.bin"

    # Set up 0 packet -- will be used a lot
    zero_packet = m.make_message_text("0")

    # Create prompt and operate
    packetcount = 0

    while (True):
        print ("Commands")
        print ("==============")
        print ("ES :: Enter PIPE mode (if you didn't already do it)")
        print ("00 :: Ping OBC")
        print ("01 :: Get RTC Date/Time")
        print ("02 :: Set RTC Date/Time")
        print ("03 :: Read OBC EEPROM")
        print ("04 :: Erase OBC EEPROM")
        print ("05 :: Read OBC RAM Byte")
        print ("06 :: Set Beacon Inhibit Enable")
        print ("10 :: Read Data Block")
        print ("11 :: Read Primary Command Blocks")
        print ("12 :: Read Secondary Command Blocks")
        print ("13 :: Read Most Recent Status Info")
        print ("14 :: Read Recent Local Data Block")
        print ("15 :: Read Raw Memory Bytes")
        print ("20 :: Collect Data Block")
        print ("21 :: Get Automatic Data Collection Settings")
        print ("22 :: Set Automatic Data Collection Enable")
        print ("23 :: Set Automatic Data Collection Period")
        print ("24 :: Resync Automatic Data Collection Timers")
        print ("30 :: Get Current Block Numbers")
        print ("31 :: Set Current Block Number")
        print ("32 :: Get Memory Section Addresses")
        print ("33 :: Set Memory Section Start Address")
        print ("34 :: Set Memory Section End Address")
        print ("35 :: Erase Memory Physical Sector")
        print ("36 :: Erase Memory Physical Block")
        print ("37 :: Erase All Memory")
        print ("40 :: Send EPS CAN Message")
        print ("41 :: Send PAY CAN Message")
        print ("42 :: Actuate PAY Motors")
        print ("43 :: Reset Subsystem")
        print ("44 :: Set Indefinite Low-Power Mode Enable")
        
        cmd =  input("\nPlease enter your command:\t").upper()
    
        if (cmd == "ES"):
            os.system("cp messages/2019-06-15-TEST/ES_PIPE.bin " + outpath)
            os.system("python2 tx/gfsk_tx_for_test_20190817.py")
            continue

        # Create actual message packet
        # FORMAT: 
        ## Byte 0 ------- Opcode
        ## Bytes 1-4 ---- Argument 1
        ## Bytes 5-8 ---- Argument 2
        ## Bytes 9-12 --- Password
        
        # Start message off with op-code
        message = cmd + " "
        
        zero_args = ["00", "01", "13", "21", "24", "30", "32", "37"]
        one_arg   = ["03", "04", "05", "06", "14", "36", "42", "43", "44"]
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
        
        # Turn into packet, pad with 2 "0" packets for safe transmission
        message += "55 54 41 54"
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

        os.system("python2 tx/gfsk_tx_for_test_20190817.py")
