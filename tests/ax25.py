def str2pkt(info, dest, src, r1=None, r2=None, ):
    if len(dest) > 6 or len(src) > 6:
        return None;
    info = [ord(c) for c in info]
    dest = [ord(c) << 1 for c in dest] + (6-len(dest))*[0x40,] + [0b01100000,]
    src  = [ord(c) << 1 for c in src]  + (6-len(src))*[0x40,]  + [0b01100000,]
    if r1 == None:
        callsigns = dest+src
    elif len(r1) > 6:
        return None
    else:
        r1 = [ord(c) << 1 for c in r1] + (6-len(r1))*[0x40,] + [0b01100000,]
        if r2 == None:
            callsigns = dest+src+r1
        elif len(r2) > 6:
            return None
        else:
            r2 = [ord(c) << 1 for c in r2] + (6-len(r2))*[0x40,] + [0b01100000,]
            callsigns = dest+src+r1+r2
    callsigns[-1] |= 1
    ctrl = [0b00000011,]
    pid = [0xF0,]
    return callsigns+ctrl+pid+info




def pkt2str(packet):
    pass
