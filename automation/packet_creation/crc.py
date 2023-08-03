"""Contains the function for calculating the crc16 value
    Functions:
        crc16_a2a(str)      :: string to string
        crc16_a2b(str)      :: string to bytes
        crc16_b2b(bytestr)  :: bytes to bytes

"""

def crc16_a2a(str):
    """Take in a string and calculate its correct crc16 value.

    Args:
        str     :: your message as a string (eg. "hello")

    Result:
        bad_crc :: correct crc16 value for your message
    """

    #Variable, constants declaration and initiation
    poly = 0x1021
    bad_crc = 0xffff

    #For each letter in the message, convert it to a binary value
    #and update the bad_crc value based on each binary value.
    for x in str:
        ch = int(format(ord(x), 'b'), 2)        #convert letter at index 'x' to a binary value using ASCII
        ch <<= 8

        #Update the bad_crc value using bitwise operations
        for i in range(8):
            if ((bad_crc ^ ch) & 0x8000):
                xor_flag = 1
            else:
                xor_flag = 0
            bad_crc = (bad_crc << 1) % 0x10000
            if xor_flag == 1:
                bad_crc = bad_crc ^ poly
            ch = ch << 1
    return bad_crc

def crc16_b2b(bytestr):
    """Take in bytes and calculate its correct crc16 value.

    Args:
        bytestr :: your message as a b'bytes' (eg. b'hello')

    Result:
        bad_crc :: correct crc16 value for your message (as bytes type)
    """

    #Variable, constants declaration and initiation
    poly = 0x1021
    bad_crc = 0xffff

    #For each letter in the message, convert it to a binary value
    #and update the bad_crc value based on each binary value.
    for ch in bytestr:
        ch <<= 8

        #Update the bad_crc value using bitwise operations
        for i in range(8):
            if ((bad_crc ^ ch) & 0x8000):
                xor_flag = 1
            else:
                xor_flag = 0
            bad_crc = (bad_crc << 1) % 0x10000
            if xor_flag == 1:
                bad_crc = bad_crc ^ poly
            ch = ch << 1

    return (bad_crc).to_bytes(2, "big")

def crc16_a2b(str):
    return crc16_a2a(str).to_bytes(2, "big")
