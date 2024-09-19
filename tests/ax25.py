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
    dest = ''.join(chr(c>>1) for c in packet[0:6]).strip()
    dest_ssid_o = packet[6]
    dest_ssid = (dest_ssid_o >> 1) & 0b1111
    packet = packet[7:]

    src = ''.join(chr(c>>1) for c in packet[0:6]).strip()
    src_ssid_o = packet[6]
    src_ssid = (src_ssid_o >> 1) & 0b1111
    packet = packet[7:]

    msg = f'\033[92m{dest}-{dest_ssid}\033[0m to {src}-{src_ssid}'
    
    if not (src_ssid_o & 1):
        r1 = ''.join(chr(c>>1) for c in packet[0:6]).strip()
        r1_ssid_o = packet[6]
        r1_ssid = (r1_ssid_o >> 1) & 0b1111
        packet = packet[7:]
        if r1_ssid_o & (1 << 8):
            msg += f' via \033[4m{r1}-{r1_ssid}\033[0m'
        else:
            msg += f' via {r1}-{r1_ssid}'
        if not (r1_ssid_o & 1):
            r2 = ''.join(chr(c>>1) for c in packet[0:6]).strip()
            r2_ssid_o = packet[6]
            r2_ssid = (r2_ssid_o >> 1) & 0b1111
            packet = packet[7:]
            if r2_ssid_o & (1 << 8):
                msg += f', \033[4m{r2}-{r2_ssid}\033[0m'
            else:
                msg += f', {r2}-{r2_ssid}'
    
    ctrl = packet[0]
    pid = packet[1]
    info = ''.join(chr(c) for c in packet[2:])
    msg += ': ' + info

    return msg


