# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#										#
# Purpose: Provide an interface for running the OBC <--> Comms Tx/Rx Link	#
# Author: Gabe Sher pls hit me up on slack @Gabe if there's an issue		#
# Date: Thursday, August 16th							#
#										#
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
        print ("00 :: Ping")
        print ("01 :: Get Subsystem Status")
        print ("02 :: Get RTC Date/Time")
        print ("03 :: Set RTC Date/Time")
        print ("04 :: Read Memory Bytes")
        print ("05 :: Erase Memory Physical Sector")
        print ("06 :: Collect Block")
        print ("07 :: Read Local Block")
        print ("08 :: Read Memory Block")
        print ("09 :: Enable/Disable Automatic Data Collection")
        print ("0A :: Set Period for Automatic Data Collection")
        print ("0B :: Resync Automatic Data Collection")
        print ("0E :: PAY Control - Actuate Motors")
        print ("0F :: Reset Subsystem")
        print ("10 :: Send CAN message - EPS")
        print ("11 :: Send CAN message - PAY")
        print ("12 :: Read EEPROM (OBC)")
        print ("13 :: Get Current Block Number")
        print ("14 :: Set Current Block Number")
        print ("15 :: Set Memory Section Start Address")
        print ("16 :: Set Memory Section End Address")
        print ("17 :: Erase EEPROM (OBC)")
        print ("19 :: Erase All Memory")
        print ("1A :: Erase Memory Physical Block")
        
        cmd =  input("\nPlease enter your command:\t").upper()
    
        if (cmd == "ES"):
            os.system("cp messages/2019-06-15-TEST/ES_PIPE.bin " + outpath)
            os.system("python2 tx/gfsk_tx_for_test_20190817.py")
            continue

        # Create actual message packet
        message = "\x00"        # Start of message
        message += "\x12"       # Size excl. this and last byte - fixed because uplink
        message += cmd          # Command type -- always just the input for this list
        if (cmd == "00" or cmd == "02" or cmd == "0B" or cmd == "19"):
            # Zero arguments -- simple

            # Create message
            message += "00"*8   # Arguments 1 and 2 -- irrelevant

        elif (cmd == "01" or cmd == "05" or cmd == "06" or cmd == "07" or cmd == "0E" or cmd == "0F" or cmd == "12" or cmd == "13" or cmd == "17" or cmd == "1A"):
            # One argument -- a bit less simple
            
            # Get argument
            print("Please input the argument in ASCII format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. Spaces are optional)")
            arg1 = input("\t")
            arg1_ascii = "".join(arg1.split())

            # Create message
            message += arg1_ascii
            message += "00"*4   # Argument 2 is just empty
        
        elif (cmd == "03" or cmd == "04" or cmd == "08" or cmd == "09" or cmd == "0A" or cmd == "10" or cmd == "11" or cmd == "14" or cmd == "15" or cmd == "16"):
            # Two arguments

            # Get argument 1
            print("Please input the FIRST argument in ASCII format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. Spaces are optional)")
            arg1 = input("\t")
            arg1_ascii = "".join(arg1.split())

            # Get argument 2
            print("Please input the SECOND argument in ASCII format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. Spaces are optional)")
            arg2 = raw_input("\t")
            arg2_ascii = "".join(arg2.split())

            # Create message
            message += arg1_ascii
            message += arg2_ascii
        else:
            print("Something went wrong, I wasn't expecting that command number.")
            print("Please try again. Make sure to select something from the list, like \"00\" or \"12\"")
            continue
        
        # Turn into packet, pad with 2 "0" packets for safe transmission
        packet = m.make_message_text(message)
        packet += zero_packet*2

        # Write to files for sending and logging
        #m.write_to_file("./"+logdir+"/packet"+str(packetcount)+".bin", packet) # Commented out because not working, oddly
        #os.system("echo 'Sent packet for command " + cmd + ", looked like:' >> " + logdir + "/log.txt")
        #os.system("echo '" + str(packet) + "' >> " + logdir + "/log.txt")
        #os.system("echo '' >> " + logdir + " /log.txt")
        m.write_to_file(outpath, packet)
        packetcount += 1

        os.system("python2 tx/gfsk_tx_for_test_20190817.py")
