import binascii, sys
filename = '../messages/alphabet_0padded.bin'
output = 'output.log'
with open(filename, 'rb') as f:
    content = f.read()

n = 0

file = open(output, 'w')
#file.write(content)
for b in content:
    
    if (n == 16):
        file.write('\n')
        n = 0
    file.write(hex(b))
    file.write(' ')
    n+=1
# s = 0
# n = 0
# for c in content:
#     if (s == 2):
#         #file.write(' ')
#         s = 0 
#     if (n == 47):
#         #file.write('\n')
#         n = 0
#     file.write(str(c))
#     print(c)
#     s+=1
#     n+=1
      

# file.close()

#print(binascii.hexlify(content), flush=True)
