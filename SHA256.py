global h0
global h1
global h2
global h3
global h4
global h5
global h6
global h7



h0 = 0x6a09e667
h1 = 0xbb67ae85
h2 = 0x3c6ef372
h3 = 0xa54ff53a
h4 = 0x510e527f
h5 = 0x9b05688c
h6 = 0x1f83d9ab
h7 = 0x5be0cd19

k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

#issue with this funcl
def add(a, b):
    result = (int(a, 2) + int(b,2)) % 4294967296
    #print(a)
    # print(int(a,2))

    # print(b)
    # print(int(b,2))
    #print(result)
    #print(result)
    #print('{:032b}'.format(result))
    return '{:032b}'.format(result)

def str_to_bin(data):
    return ''.join(format(ord(i),'b').zfill(8) for i in data)

def hex_to_bin(data):
    #print(str(0x6a09e667))
    return '{:032b}'.format(int(str(data), 10))

#cuz im too lazy to convert string representation of binary into actual binary
def bitwiseXOR(arg1, arg2):
    result = ""
    #print(len(arg1) - len(arg2))
    # print(len(arg2))
    for i in range(0, len(arg1)):
        if (int(arg1[i])+int(arg2[i]) == 2):
            result+='0'
        else:
            result+=str(int(arg1[i])+int(arg2[i]))
    #print(len(result) - len(arg1))      
    return result

def rotate(data, rot):
    # neg num for right rotation
    a = len(data)
    result = data[rot:] + data[:rot]
    #print(a - len(result))
    return result

def bitNOT(data):
    a = len(data)
    result = ""
    for i in range(0, len(data)):
        if (int(data[i])==1):
            result+="0"
        else:
            result+="1"
    #print(a- len(result))
    return result


#broken here
def bitwiseAND(arg1, arg2):
    # a = len(arg1) - len(arg2)
    # print(a)
    result=""
    for i in range(0, len(arg1)):
        if (int(arg1[i])+int(arg2[i])==2):
            result += "1"
        else:
            result +="0"
    return result

def rightSHIFT(data, shift):
    #a = len(data)
    #print(a - len(shift*"0" + data[:-shift]))
    return shift*"0" + data[:-shift]

def SHA256HASH(data):
    w = str_to_bin(data)
    bigEnd = len(w)
    w += "1"
    lengthOfBin = len(w)
    w += "0"*(448-lengthOfBin)
    bigEnd = bin(bigEnd)[2:]
    w += "0"*(64-len(bigEnd))
    w += bigEnd
    w += 1536*"0"
    w = [w[i:i+32] for i in range(0, len(w), 32)]
    #print(len(h))
    
    for i in range(16, 64):
        s0 = bitwiseXOR(bitwiseXOR(rotate(w[i-15], -7), rotate(w[i-15], -18)), rightSHIFT(w[i-15], 3)) 
        s1 = bitwiseXOR(bitwiseXOR(rotate(w[i-2], -17), rotate(w[i-2], -19)), rightSHIFT(w[i-2], 10)) 
        w[i] = add(add(w[i-16], s0), add(w[i-7], s1))
        if (i == 16):
            print(w[0])
            print(s0)
            print(w[9])
            print(s1)
            print(w[16])
    global h0
    global h1
    global h2
    global h3
    global h4
    global h5
    global h6
    global h7
    h0 = hex_to_bin(h0)
    h1 = hex_to_bin(h1)
    h2 = hex_to_bin(h2)
    h3 = hex_to_bin(h3)
    h4 = hex_to_bin(h4)
    h5 = hex_to_bin(h5)
    h6 = hex_to_bin(h6)
    h7 = hex_to_bin(h7)

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    f = h5
    g = h6
    h = h7
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)
    # print(f)
    # print(g)
    # print(h)
    # print(rotate(e, -6))
    # print(rotate(e, -11))
    # print(rotate(e, -25))
    for i in range(0, 64):
            
            S1 = bitwiseXOR(bitwiseXOR(rotate(e,-6), rotate(e,-11)), rotate(e,-25))
            
            ch = bitwiseXOR(bitwiseAND(e,f),(bitwiseAND(bitNOT(e), g)))
            #temp1 = h + s1 + ch + k[i] + w[i]
            #temp1 = add(add(add(h,S1), ch), add(hex_to_bin(k[i]),w[i]))
            temp1 = add(add(add(h, S1), ch), add(hex_to_bin(k[i]), w[i]))
            #temp1 = hex_to_bin(k[i])
            
            S0 = bitwiseXOR(bitwiseXOR(rotate(a,-2), rotate(a,-13)),rotate(a,-22))
            maj = bitwiseXOR(bitwiseXOR(bitwiseAND(a,b), bitwiseAND(a,c)), bitwiseAND(b,c))
            temp2 = add(S0, maj)
            
            h = g
            g = f
            f = e
            e = add(d, temp1)
            d = c
            c = b
            b = a
            a = add(temp1, temp2)
            # if i == 0:
            #     print(h)
            #     print(g)
            #     print(f)
            #     print(e)
            #     print(d)
            #     print(c)
            #     print(b)
            #     print(a)
    h0 = add(h0, a)
    h1 = add(h1, b)
    h2 = add(h2, c)
    h3 = add(h3, d)
    h4 = add(h4, e)
    h5 = add(h5, f)
    h6 = add(h6, g)
    h7 = add(h7, h)
    finalHash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    return hex(int(finalHash, 2))