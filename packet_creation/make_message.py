"""
Functions:
    make_message_text(message, preamble=b'\x55', carriage=False)
    make_message_hex(message, preamble=b'\x55', carriage=False) **UNIMPLEMENTED**
    encode_message(dec_msg)
    write_to_file(filename, message)
"""

from packet_creation import crc

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
    assert(length < 128)

    # Create message
    transmission = preamble * 25                        # preamble
    transmission += b'\x7E'                             # sync word
    transmission += length.to_bytes(1, "big")           # size byte

    msg_for_crc  = length.to_bytes(1, "big").decode()   # prep for checksum calculation

  #  msg_for_crc += message
   # msg_for_transmission += message
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
    transmission = preamble * 25                # preamble
    transmission += b'\x7E'                     # sync word
    transmission += length.to_bytes(1, "big")   # size byte
    transmission += message                     # the (should-be) encoded message content

    msg_for_crc  = length.to_bytes(1, "big")
    msg_for_crc  += message
    
    if (carriage):                              # carriage return
        msg_for_crc  += '\x0D'
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
        dec_msg :: decoded message as ASCII text
    """
    enc_msg = []    # Convert to bytes later

    # 64 bit integer that will hold the 56 bit values from the byte groups
    base_conversion_buff = 0
    # Number of 7 byte groups in the decoded message
    num_byte_groups = len(dec_msg) // 7
    # Number of bytes leftover
    num_remainder_bytes = len(dec_msg) % 7
    # Encoded length
    enc_len = (num_byte_groups * 8 + num_remainder_bytes + 1) if (num_remainder_bytes > 0) else (num_byte_groups * 8)

    # All encoded messages start with 0x00
    enc_msg.append(0)
    # Next field is the length. This value will later be mapped similar to the other bytes.
    enc_msg.append(enc_len + 0x10)
    enc_msg.append(0)

    # Set up array of powers of 254
    # [0] = 254^0, [7] = 254^7
    pow_254 = [0 for i in range(8)]
    pow_254[0] = 1
    for i in range(1, 8):
        pow_254[i] = pow_254[i - 1] * 254

    # Convert each of the 7 base-256 digits to 8 base-254 digits
    for i_group in range(0, num_byte_groups):
        base_conversion_buff = 0

        for i_byte in range(0, 7):
            base_conversion_buff += dec_msg[ (7 * i_group) + i_byte] * (1 << ((6 - i_byte) * 8))

        for i_byte in range(0, 8):
            enc_msg.append((base_conversion_buff // pow_254[7 - i_byte]) % 254)


    # encode the remainining bytes
    if(num_remainder_bytes > 0):
        base_conversion_buff = 0
        for i_byte in range(0, num_remainder_bytes):
            base_conversion_buff += dec_msg[num_byte_groups*7 + i_byte] * (1 << ((num_remainder_bytes - 1 - i_byte) * 8))

        for i_byte in range(0, num_remainder_bytes + 1):
            enc_msg.append((base_conversion_buff // pow_254[num_remainder_bytes - i_byte]) % 254)


    # Perform the mapping to avoid values 0 and 13. 0-11 -> 1-12, 12-253 -> 14-255
    # Note that the length of the message is not put through this mapping. The other digit that doesn't get mapped is the 0x00.
    for i in range(3, 3 + enc_len):
        if( enc_msg[i] >= 0 and enc_msg[i] <= 11 ):
            enc_msg[i] += 1

        elif( enc_msg[i] >= 12 and enc_msg[i] <= 253 ):
            enc_msg[i] += 2

    enc_msg.append(0x00)

    return bytes(enc_msg)


def decode_message(enc_msg):
    # Easier to work with encoded message as a list of ints rather than bytes
    enc_msg = list(enc_msg)
    dec_msg = []

    # length of base-254 encoded message can be extracted from the first field, the mapping is undone
    enc_len = enc_msg[1] - 0x10
    # 64 bit integer that will hold the 56 bit values from the byte group
    base_conversion_buff = 0
    # concatenate the message into 8 byte groups and leftovers, then calculate length
    num_byte_groups = enc_len // 8
    num_remainder_bytes = enc_len % 8

    # TODO - what if 1 remainder byte?
    if (num_remainder_bytes == 0):
        dec_len = num_byte_groups * 7
    else:
        dec_len = (num_byte_groups * 7) + (num_remainder_bytes - 1)

    # unmap the values in the buffer
    for i in range(0, enc_len):
        if(enc_msg[3 + i] >= 1 and enc_msg[3 + i] <= 12):
            enc_msg[3 + i] -= 1
        elif(enc_msg[3 + i] >= 14 and enc_msg[3 + i] <= 255):
            enc_msg[3 + i] -= 2


    # Set up array of powers of 254
    # [0] = 254^0, [7] = 254^7
    pow_254 = [0x00 for i in range(8)]
    pow_254[0] = 1
    for i in range(1, 8):
        pow_254[i] = pow_254[i - 1] * 254

    for i_group in range(0, num_byte_groups):
        base_conversion_buff = 0

        for i_byte in range(0, 8):
            base_conversion_buff += enc_msg[ 3 + (8 * i_group) + i_byte ] * pow_254[7 - i_byte]

        for i_byte in range(0, 7):
            dec_msg.append((base_conversion_buff // (1 << ((6 - i_byte) * 8))) % 256)

    if (num_remainder_bytes > 1):
        base_conversion_buff = 0
        for i_byte in range(0, num_remainder_bytes):
            base_conversion_buff += enc_msg[ 3 + (num_byte_groups * 8) + i_byte ] * pow_254[num_remainder_bytes - 1 - i_byte]

        for i_byte in range(0, num_remainder_bytes - 1):
            dec_msg.append((base_conversion_buff // (1 << ((num_remainder_bytes - 2 - i_byte) * 8))) % 256)

    return bytes(dec_msg)


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
                        trx += make_message_text(msg, carriage=True)
                    else:
                        trx += make_message_text(msg, carriage=False)
                else:
                    trx += make_message_text(msg, carriage=True)

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
                write_to_file("../messages"+filename, trx)
                print("\nWrote", trx, "to file", filename)
            else:
                print("OK.")

        else:
            break

if __name__ == "__main__":
    main()
