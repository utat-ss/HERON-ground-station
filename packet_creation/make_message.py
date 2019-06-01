"""
Functions:
    make_message_text(message, preamble=b'\x55', carriage=False)
    make_message_hex(message, preamble=b'\x55', carriage=False) **UNIMPLEMENTED**
    write_to_file(filename, message)
"""

from crc import crc16

def make_message_text(message, preamble=b'\x55', carriage=False):
    """Make a message as a binary value. Adds preamble, syncword, message and checksum together.

    Args:
        message  :: your message to send, as a string (e.g. "hello")
        preamble :: either b'\\xaa' or b'\\x55'
        carriage :: whether or not you would like to append a carriage return to your message
    Result:
        message  :: bitstring of full message/messages for transmission
    """
    # Get length
    length = len(message)
    if (carriage):
        length += 1

    # Assertions for inputs
    assert(preamble==b'\x55' or preamble==b'\xaa')
    assert(length < 256)

    # Create message
    transmission = preamble * 5                 # preamble
    transmission += b'\x7E'                     # sync word
    transmission += length.to_bytes(1, "big")   # size byte

    msg_for_crc  = str(length)                  # prep for checksum calculation

    for ch in message:                          # actual message
        msg_for_crc  += ch
        transmission += ord(ch).to_bytes(1, "big")

    if (carriage):                              # carriage return
        msg_for_crc  += '\x0D'
        transmission += b'\x0D'

    transmission += crc16_bytes(msg_for_crc)    # checksum

    return transmission

def write_to_file(filename, message):
    """Writes a message to a binary file.

    Args:
        filename :: name of file, e.g. "hello_55.bin" ("hello" with 0x55 as the preamble)
        message  :: output from make_message()
    """
    if (filename.find('/') != -1):
        filename = filename.split('/')[-1]
    with open("messages/"+filename, "wb") as f:
        f.write(message)

def main():
    preamble_type = b'\x55'
    automatic_cr  = False
    while (true):
        action = ""
        while (action != "s" and action != "m" and action != "q"):
            action = input("Would you like to make one or more messages (m), change the settings (s), or quit (q):\n\t")
        if (action == "s"):
            print("1. Change preamble")
            if (automatic_cr):
                print("2. Toggle prompting/automatic carriage return (currently automatic)")
            else:
                print("2. Toggle prompting/automatic carriage return (currently prompting)")
            print("3. Cancel\n\n==========================")

            action = input("Please enter the number corresponding to your desired action:\n\t")
            if (action == "1"):
                action = input("Please enter A or 0xAA or 5 for 0x55:\n\t")
                if (action == "5"):
                    preamble_type = b'\x55'
                elif (action == "a" or action == "A"):
                    preamble_type = b'\xaa'
                else:
                    print("Invalid input")
            elif (action == "2"):
                automatic_cr = not automatic_cr
            else:
                print("Invalid input")
            print ("Done.\n")
        elif (action == "m"):
            writing_more = True
            trx = b''
            while (writing_more):
                msg = input("Please write your message:\n\t")
                if (not automatic_cr):
                    while (action != 'y' and action != 'n'):
                        action  = input("Do you want to append a carraige return character? (y/n)\n\t")
                    if (action == 'y'):
                        trx += make_message_text(msg, carriage=True)
                    else:
                        trx += make_message_text(msg, carriage=False)
                else:
                    trx += make_message_text(msg, carriage=True)

                print("Your message is:\n\t", trx)

                while (writing_more != 'y' and writing_more != 'n'):
                    writing_more = input("Would you like to append another message (same transmission)? (y/n)")
                if (writing_more == 'y');
                    writing_more = True
                else:
                    writing_more = False

            # Write to file
            action = ''
            while (action != 'y' and action != 'n'):
                action = input("Would you like to write this transmission to a file? (y/n)\n\t")
            if (action == 'y'):
                filename = input("Please enter your filename (e.g. file.bin):\n\t")
                write_to_file(filename, trx)
                print("Wrote", trx, "to file", filename)
            else:
                print("OK.")

        else:
            break

if __name__ == "__main__":
    main()
