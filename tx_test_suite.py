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
        print ("01 :: Get RTC Date/Time")
        print ("02 :: Set RTC Date/Time")
        print ("03 :: Read OBC EEPROM") 
        print ("04 :: Erase OBC EEPROM")
        print ("05 :: Read OBC RAM Byte")
        print ("06 :: Send EPS CAN Message")
        print ("07 :: Send PAY CAN Message")
        print ("08 :: Actuate PAY Motors")
        print ("09 :: Reset Subsystem")
        print ("0A :: Set Indefinite Low-Power Mode Enable")
        print ("10 :: Read Most Recent Status Info")
        print ("11 :: Read Data Block")
        print ("12 :: Read Recent Local Data Block")
        print ("13 :: Read Primary Command Blocks")
        print ("14 :: Read Secondary Command Blocks")
        print ("15 :: Read Raw Memory Bytes")
        print ("16 :: Erase Memory Physical Sector")
        print ("17 :: Erase Memory Physical Block")
        print ("18 :: Erase All Memory")
        print ("20 :: Collect Data Block")
        print ("21 :: Get Current Block Number")
        print ("22 :: Set Current Block Number")
        print ("23 :: Get memory Section Start Address")
        print ("24 :: Set memory Section Start Address")
        print ("25 :: Get memory Section End Address")
        print ("26 :: Set memory Section End Address")
        print ("27 :: Get Automatic Data Collection Enable")
        print ("28 :: Set Automatic Data Collection Enable")
        print ("29 :: Get Automatic Data Collection Period")
        print ("2A :: Set Automatic Data Collection Period")
        print ("2B :: Get Automatic Data Collection Timers")
        print ("2C :: Resync Automatic Data Collection Timers"
        
        cmd =  input("\nPlease enter your command:\t").upper()
    
        if (cmd == "ES"):
            os.system("cp messages/2019-06-15-TEST/ES_PIPE.bin " + outpath)
            os.system("python2 tx/gfsk_tx_for_test_20190817.py")
            continue

        # Create actual message packet
        message = "\x00"        # Start of message
        message += "\x12"       # Size excl. this and last byte - fixed because uplink
        dec_msg = cmd           # Command type -- always just the input for this list
        if (cmd == "00" or cmd == "02" or cmd == "0B" or cmd == "19"):
            # Zero arguments -- simple

            # Create message
            dec_msg += "00"*8   # Arguments 1 and 2 -- irrelevant

        elif (cmd == "01" or cmd == "05" or cmd == "06" or cmd == "07" or cmd == "0E" or cmd == "0F" or cmd == "12" or cmd == "13" or cmd == "17" or cmd == "1A"):
            # One argument -- a bit less simple
            
            # Get argument
            print("Please input the argument in ASCII format:")
            print(" (e.g. \"00 00 00 01\" for 0x01 or \"00 00 FF FF\" for 65535. Spaces are optional)")
            arg1 = input("\t")
            arg1_ascii = "".join(arg1.split())
            
            n = 8 
            tot = 0
            for letter in arg1_ascii:
                n = n-1
                if (letter == 'A' or letter == 'B' or letter == 'C' or letter == 'D' or letter == 'E' or letter = 'F'):
                    tot += pow((letter-ord('A')+10), n)
                elif (letter == 'a' or letter == 'b' or letter == 'c' or letter == 'd' or letter == 'e' or letter = 'f'):
                    tot += pow((letter-ord('a')+10), n)
                elif (letter == '0' or letter == '1' or letter == '2' or letter == '3' or letter == '4' or letter == '5' or letter == '6' or letter == '7' or letter == '8' or letter == '9'):
                    tot += pow((letter-ord('0')), n)

                        
            # Create message
            message += arg1_ascii
            message += "00"*4   # Argument 2 is just empty
        
        elif (cmd == "03" or cmd == "04" or cmd == "08" or cmd == "09" or cmd == "0A" or cmd == "10" or cmd == "11" or cmd == "14" or cmd == "15" or cmd == "16"):
            # Two arguments

            # Get argument 1
            print("Please input the FIRST 4-byte argument in HEX format:")
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
        packet += zero_packet*3

        # Write to files for sending and logging
        #m.write_to_file("./"+logdir+"/packet"+str(packetcount)+".bin", packet) # Commented out because not working, oddly
        #os.system("echo 'Sent packet for command " + cmd + ", looked like:' >> " + logdir + "/log.txt")
        #os.system("echo '" + str(packet) + "' >> " + logdir + "/log.txt")
        #os.system("echo '' >> " + logdir + " /log.txt")
        m.write_to_file(outpath, packet)
        packetcount += 1

        os.system("python2 tx/gfsk_tx_for_test_20190817.py")
