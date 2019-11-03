from packet_creation import make_message as m

def interpret_debug(string):
    a = string.split()
    array = [int(x, 16) for x in a]
    return bytes(array)

def interpret_utat(string):
    a = string.split()
    array = [int(x, 16) for x in a]
    return m.decode_message(array)

