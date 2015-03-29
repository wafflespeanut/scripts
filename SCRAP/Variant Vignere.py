from math import ceil

fin="CTEXT.txt"; fout="CTEXT.txt"

# Known letter frequencies
fre = {97: 8.2, 98: 1.5, 99: 2.8, 100: 4.3, 101: 12.7, 102: 2.2, 103: 2.0, 104: 6.1, 105: 7.0, 106: 0.2, 107: 0.8, 108: 4.0, 109: 2.4, 110: 6.7, 111: 1.5, 112: 1.9, 113: 0.1, 114: 6.0, 115: 6.3, 116: 9.1, 117: 2.8, 118: 1.0, 119: 2.4, 120: 0.2, 121: 2.0, 122: 0.1}

def hexor(ch,k): return ord(ch.decode('hex'))^ord(k.decode('hex'))

# It deviates from the usual Vigenere in that it XORs hexed plaintext & key

def cipher(ch):
    with open(fin,'r') as file: data=file.readlines()
    if ch=='e': ptext=[format(ord(i),'02x') for i in data[0]]
    elif ch=='d': ptext=[data[0][i:i+2] for i in range(0,len(data[0]),2)]
    else: print 'Invalid option!'; return None
    k=[]; [k.extend(key) for i in range(int(ceil(len(ptext)/float(len(key)))))]
    if ch=='e': s=[format(hexor(ptext[i],k[i]),'02x') for i in range(len(ptext))]
    elif ch=='d': s=[chr(hexor(ptext[i],k[i])) for i in range(len(ptext))]
    with open(fout,'w') as file: file.writelines(''.join(s))
