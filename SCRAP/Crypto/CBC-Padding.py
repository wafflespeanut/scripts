execfile("Oracle.py")
import os,sys
from time import sleep

# A server knows the key. Our job is to find the key by sending & receiving packets...

def hexed(p): return ''.join([format(i,'02x').upper() for i in p])

def read(File,blocks):      # Our ciphertext had 3 blocks appended as IV|C1|C2
    with open(File,'r') as file: data=file.readlines()
    s=data[0]; c=len(s)/blocks
    return [s[i:i+c] for i in range(0,len(s),c)]

def test(data,blocks):   # Usage: `python Padding.py <filename>`
    ctext=[(int(data[i:i+2],16)) for i in range(0,len(data),2)]
    print "\nCTEXT:",ctext,'\n\nSending ciphertext...'
    try: rc=send(ctext,blocks)
    except IndexError: return None
    print "Oracle returned: %d\n" %(rc); return rc

def analyze(File='CBC.txt',b=3):
    data=read(File); co=connect()
    if co==-1: 'Connection failed!'; return
    rc=test(''.join(data),b); p=data[b-2]
    print 'Oracle responds!'
    p=[p[i:i+2] for i in range(0,len(p),2)]
    print 'Chosen block:',p; i=0
    while True:    # nth block is padded using PKCS #5, and so modify (n-1)th block to find key length!
        p[i]='00'; data[b-2]=''.join(p)
        print 'Modified block:',p,'\nPosition:',i+1
        if not test(''.join(data),b): break
        sleep(1); i+=1
    disconnect(); print 'Last %d bytes are padded!'%(len(p)-i)
    return i

def find(File='CBC.txt',b=3):
    l=5; data=read(File,b); k=data[b-2]; co=connect(); a={}
    if co==-1: print 'Connection failed!'; return
    for j in range(l):
        p=len(k)/2-l+j; print 'Padding key: %s (%s)'%(p,format(p,'02x').upper())
        k=[int(k[i:i+2],16) if i<2*(l-j) else int(k[i:i+2],16)^p^(p+1) for i in range(0,len(k),2)]
        i=l-(j+1); t=k[i]; k[i]=0; sleep(5)
        while True:
            data[b-2]=hexed(k); print 'Modified block:',data[b-2]
            rc=test(''.join(data),b)
            if rc==None: connect(); print 'Retrying...'; continue
            k[i]+=1
            if rc==1: k[i]-=1; a[i]=p^(t^k[i]); k=hexed(k); break
    disconnect(); return k

##if len(sys.argv)>=2: test(sys.argv[1])
##else: test()
