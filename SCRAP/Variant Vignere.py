from math import ceil
from os import path

fin="CTEXT.txt"; fout="YAY.txt"
freq='FREQ.txt' # Generated using data from a known text corpus
key=[] # Key in hex byte strings

def read(f=fin):
    with open(f,'r') as file: return file.readlines()

def write(s,f=fout):
    with open(f,'w') as file: file.writelines(s)

def hexor(ch,k): return ord(ch.decode('hex'))^ord(k.decode('hex'))

# It deviates from the usual Vigenere in that it XORs hexed plaintext & key

def IC(ls):          # Find the index of coincidences
    data=read(); ctext=[data[0][i:i+2] for i in range(0,len(data[0]),2)]; avg=0
    for k in range(ls):
        s=[ctext[i] for i in range(k,len(ctext),ls)]; d={}
        for i in set(ctext): d[i]=s.count(i)
        ic=sum([d[i]*(d[i]-1) for i in d])/(float(len(s))*(len(s)-1))
        print 'Sequence %d (length=%d): %f'%(k+1,len(s),ic); avg+=ic
    return avg/ls

def analyze(rmin=2,rmax=13):        # Find the ICs for a range of keyspaces
    d=[0,0]
    for k in range(rmin,rmax):
        print '\nAssuming keyspace=%d...\n'%(k)
        avg=IC(k); print '\n\tAverage IC: %f'%(avg)
        if avg>d[1]: d[1]=avg; d[0]=k
    print '\nHighest IC achieved: %f (for keyspace=%d)'%(d[1],d[0])
    return d[0]

def snoop():
    ksp=7; fread=read(freq); d=dict(enumerate([0 for i in range(128)]))
    for i in fread: m=i.split('\t'); d[int(m[0])]=float(m[1][:-1])
    return dfreq

def cipher(ch):
    data=read(); k=[]
    if ch=='e': ptext=[format(ord(i),'02x') for i in data[0]]
    elif ch=='d': ptext=[data[0][i:i+2] for i in range(0,len(data[0]),2)]
    else: print 'Invalid option!'; return None
    [k.extend(key) for i in range(int(ceil(len(ptext)/float(len(key)))))]
    if ch=='e': s=[format(hexor(ptext[i],k[i]),'02x') for i in range(len(ptext))]
    elif ch=='d': s=[chr(hexor(ptext[i],k[i])) for i in range(len(ptext))]
    print ''.join(s); #write(''.join(s))
