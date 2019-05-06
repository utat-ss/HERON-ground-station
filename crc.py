def crc16(str):
    poly = 0x1021
    bad_crc = 0xffff
    for x in str:
        ch = int(format(ord(x), 'b'), 2)
        ch <<= 8
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


