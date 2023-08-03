"""
Functions:
    es_frame_text(message, preamble=b'\x55', carriage=False)
    es_frame_hex(message, preamble=b'\x55', carriage=False) **UNIMPLEMENTED**
    encode_message(dec_msg)
    write_to_file(filename, message)
"""

from packet_creation import crc

def es_frame_text(message, preamble=b'\x55', carriage=False):
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
    assert(length < 128)

    # Create message
    transmission = preamble * 5                         # preamble
    transmission += b'\x7E'                             # sync word
    transmission += length.to_bytes(1, "big")           # size byte

    msg_for_crc  = length.to_bytes(1, "big").decode()   # prep for checksum calculation

    for ch in message:                                  # actual message
        msg_for_crc  += ch
        transmission += ord(ch).to_bytes(1, "big")

    if (carriage):                                      # carriage return
        msg_for_crc  += '\x0D'
        transmission += b'\x0D'

    transmission += crc.crc16_a2b(msg_for_crc)        # checksum

    return transmission

def es_frame_bytes(message, preamble=b'\x55', carriage=False):
    """Makes an ES packet as bytes from bytes. Adds preamble, syncword, message and checksum together.

    Args:
        message  :: your bytes-type string of the encoded message 
        preamble :: either b'\\xaa' or b'\\x55'
        carriage :: whether or not you would like to append a carriage return to your message
    Result:
        message  :: bitstring of one full packet for transmission
    """

    # Get length
    length = len(message)
    if (carriage):
        length += 1

    # Assertions for inputs
    assert(preamble==b'\x55' or preamble==b'\xaa')
    assert(length < 128)

    # Create message
    transmission = preamble * 5                 # preamble
    transmission += b'\x7E'                     # sync word
    transmission += length.to_bytes(1, "big")   # size byte
    transmission += message                     # the "encoded" message content

    msg_for_crc  = length.to_bytes(1, "big")    # size byte
    msg_for_crc  += message                     # the "encoded" message content
    
    if (carriage):                              # carriage return
        msg_for_crc  += b'\x0D'
        transmission += b'\x0D'

    transmission += crc.crc16_b2b(msg_for_crc)  # checksum

    return transmission

def write_to_file(filename, message):
    """Writes a message to a binary file.

    Args:
        filename :: name of file, e.g. "hello_55.bin" ("hello" with 0x55 as the preamble)
        message  :: output from make_message()
    """
    if (filename.find('/') != -1):
        filename = filename.split('/')[-1]
    with open(filename, "wb") as f:
        f.write(message)

def encode_message(dec_msg):
    """Applies UTAT encoding scheme to a message.
    
    Args:
        dec_msg :: decoded message as an array of int ASCII values
    """
    TRANS_PKT_DELIMITER = 0x55
    dec_len = len(dec_msg)
    enc_len = dec_len + 9
    
    enc_msg = [0x00] * enc_len    # Convert to bytes later


    checksum_buf = [0x00]*(15+1) # TRANS_RX_DEC_MSG_MAX_SIZE + 1
    checksum_buf[0] = dec_len
    i = 0
    while i < dec_len and (1+i) < len(checksum_buf):
        checksum_buf[1+i] = dec_msg[i]
        i += 1
    checksum = crc32(checksum_buf, 1 + dec_len)

    # All encoded messages start with 0x55
    enc_msg[0] = TRANS_PKT_DELIMITER
    # Next field is the length. This value will later be mapped similar to the other bytes.
    enc_msg[1] = dec_len
    enc_msg[2] = TRANS_PKT_DELIMITER
    for i in range(dec_len):
        enc_msg[3+i] = dec_msg[i]

    enc_msg[enc_len - 6] = TRANS_PKT_DELIMITER
    enc_msg[enc_len - 5] = (checksum >> 24) & 0xFF
    enc_msg[enc_len - 4] = (checksum >> 16) & 0xFF
    enc_msg[enc_len - 3] = (checksum >> 8) & 0xFF
    enc_msg[enc_len - 2] = (checksum >> 0) & 0xFF
    enc_msg[enc_len - 1] = TRANS_PKT_DELIMITER

    return bytes(enc_msg)

def get_uint32(num):
    while num < 0:
        num += (1 << 32)
    while num >= (1 << 32):
        num -= (1 << 32)
    return num

def crc32(message, len):
    crc = 0xFFFFFFFF

    i = 0
    while i < len:
        byte = message[i]
        crc = crc ^ byte
        for j in range (0, 8):
            mask = get_uint32(-(crc & 1))
            crc = (crc >> 1) ^ (0xEDB88320 & mask)
        i = i + 1

    crc = get_uint32(~crc)

    return crc 

def main():
    preamble_type = b'\x55'
    automatic_cr  = False
    while (1==1):
        action = ""
        while (action != "s" and action != "m" and action != "q"):
            action = input("\nWould you like to make one or more messages (m), change the settings (s), or quit (q):\n\t")
        if (action == "s"):
            # Settings menu
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
            # Creating a new transmission (message or string of messages)
            writing_more = True
            trx = b''
            while (writing_more):
                msg = input("Please write your message:\n\t")
                if (not automatic_cr):
                    #action = ''            # Comment out if you want it to be easier to make a transmission of many messages WITHOUT a CR
                    while (action != 'y' and action != 'n'):
                        action  = input("Do you want to append a carraige return character? (y/n)\n\t")
                    if (action == 'y'):
                        trx += es_frame_text(msg, carriage=True)
                    else:
                        trx += es_frame_text(msg, carriage=False)
                    action = ''
                else:
                    trx += es_frame_text(msg, carriage=True)

                #print("Your message is:\n\t", trx)

                while (writing_more != 'y' and writing_more != 'n'):
                    writing_more = input("Would you like to append another message (same transmission)? (y/n)\n\t")
                if (writing_more == 'y'):
                    writing_more = True
                else:
                    writing_more = False

            # Write to file
            action = ''
            while (action != 'y' and action != 'n'):
                action = input("Would you like to write this transmission to a file? (y/n)\n\t")
            if (action == 'y'):
                filename = input("Please enter your filename (e.g. file.bin):\n\t")
                write_to_file("../messages/"+filename, trx)
                print("\nWrote", trx, "to file", filename)
            else:
                print("OK.")

        else:
            break

if __name__ == "__main__":
    main()
