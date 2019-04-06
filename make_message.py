"""
Function 'prototypes':
    make_message(message, checksum, preamble=b'\x55')
    write_to_file(filename, message)
"""

def make_message(message, checksum, preamble=b'\x55'):
    """Make a message as a binary value. Adds preamble, syncword, message and checksum together.

    Args:
        bits     :: your message to send, as a string (e.g. "hello")
        checksum :: 2 byte bistring like b'\\xFF\\xFF'
        preamble :: either b'\\xaa' or b'\\x55'

    Result:
        message  :: bitstring of full message for transmission
    """
    # Assertions for inputs
    assert(preamble==b'\x55' or preamble==b'\xaa')
    assert(len(message) < 256)
    assert(len(checksum) == 2)

    # Create message
    transmission = preamble * 5 # preamble
    transmission += b'\x7E'     # sync word
    transmission += len(message).to_bytes(1, "big")
                                # size byte
    #msg_for_crc = len(message).to_bytes(1, "big")
    for ch in message:          # actual message
        #msg_for_crc += ord(ch).to_bytes(1, "big")
        transmission += ord(ch).to_bytes(1, "big")
    transmission += checksum    # checksum
    #transmission += crc(msg_for_crc)

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
    action = ""
    while (action != "s" and action != "m"):
        action = input("Would you like to send a message (m) or change the settings (s):\n\t")
    if (action == "s"):
        print("1. Change preamble\n\n===========================")
        action = input("Please enter the number corresponding to your desired action:\n\t")
        if (action == "1"):
            action = input("Please enter A or 0xAA or 5 for 0x55:\n\t")
            if (action == "5"):
                preamble_type = b'\x55'
            elif (action == "a" or action == "A"):
                preamble_type = b'\xaa'
            else:
                print("Invalid input")
        else:
            print("Invalid input")
    elif (action == "m"):
        msg = input("Please write your message:\n\t")
        chk = input("Please write your checksum, in hex (e.g. 0x1A7D)\n\t")
        if (len(chk) > 6):
            print("Invalid input")
        if (chk[1] == 'x'):
            chk = chk[2:]
        if (len(chk) > 4):
            print("Invalid input")
        chk = int(chk, 16).to_bytes(2, "big")

        trx = make_message(msg, chk, preamble_type)

        print("Your output is:\n\t", trx)
        while (action != 'y' and action != 'n'):
            action = input("Would you like to write this to a file? (y/n)\n\t")
        if (action == 'y'):
            filename = input("Please enter your filename (e.g. file.bin):\n\t")
            write_to_file(filename, trx)
            print("Wrote", trx, "to file", filename)
        else:
            print("OK.")

if __name__ == "__main__":
    main()
