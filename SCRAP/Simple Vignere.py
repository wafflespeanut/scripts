from math import ceil

fin="CTEXT.txt"; fout="TEMP.txt"; key='A12F'
# This is just to solve a problem. "Simple" because it reads only the first line...

def xor(ch,k): return ord(ch)^ord(k)

def cipher(ch):
    s=[]; j=0; k=[]
    with open(fin,'r') as file: data=file.readlines()
    if ch=='e':
        k=''.join([key for i in range(int(ceil(len(data[0])/float(len(key)))))])
        s=[format(xor(data[0][i],k[i]),'02x') for i in range(len(data[0]))]
    elif ch=='d':
        k=''.join([key for i in range(int(ceil(len(data[0])/float(len(key)))/2))])
        for i in range(0,len(data[0]),2):
            s.append(chr(xor(data[0][i:i+2].decode('hex'),k[j]))); j+=1
    else: print 'Unknown option!'; return None
    print ''.join(s)
##    with open(fout,'w') as file: file.writelines(''.join(s))
