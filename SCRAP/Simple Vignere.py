from math import ceil

fin="CTEXT.txt"; fout="CTEXT.txt"; key=['A1','2F']
# This is just to solve a problem. "Simple" because it reads only the first line...

def xor(ch,k): return ord(ch)^ord(k)

# It deviates from the usual Vigenere in that it XORs hexed plaintext & key

def cipher(ch):
    with open(fin,'r') as file: data=file.readlines()
    if ch=='e': ptext=[format(ord(i),'02x') for i in data[0]]
    elif ch=='d': ptext=[data[0][i:i+2] for i in range(0,len(data[0]),2)]
    else: print 'Invalid option!'; return None
    k=[]; [k.extend(key) for i in range(int(ceil(len(ptext)/float(len(key)))))]
    if ch=='e':
        s=[format(xor(ptext[i].decode('hex'),k[i].decode('hex')),'02x') for i in range(len(ptext))]
        with open(fout,'w') as file: file.writelines(''.join(s).upper())
    elif ch=='d':
        s=[chr(xor(ptext[i].decode('hex'),k[i].decode('hex'))) for i in range(len(ptext))]
        with open(fout,'w') as file: file.writelines(''.join(s))
