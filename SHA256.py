def SHA256HASH(data):
    h = ' '.join(format(ord(x), 'b') for x in data)
    print(h)