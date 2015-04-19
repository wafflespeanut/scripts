execfile("Oracle.py")
import os
from time import sleep

# A server knows the key. Our job is to find the key by sending & receiving packets...

def hexed(p): return ''.join([format(i,'02x').upper() for i in p])

def read(File,blocks=3):         # Our ciphertext had 3 blocks appended as IV|C1|C2
    with open(File,'r') as file: data=file.readlines()
    s=data[0]; c=len(s)/blocks
    return [s[i:i+c] for i in range(0,len(s),c)]

def test(data,blocks=3):         # Usage: `python Padding.py <filename>`
    ctext=[(int(data[i:i+2],16)) for i in range(0,len(data),2)]
    print "\nCTEXT:",ctext,'\n\nSending ciphertext...'
    rc=send(ctext,blocks)
    print "Oracle returned: %d\n" %(rc); return rc

def analyze(File='CBC.txt'):
    data=read(File); co=connect()
    if co==-1: 'Connection failed!'; return
    rc=test(''.join(data)); p=data[-2]
    print 'Oracle responds!'
    p=[p[i:i+2] for i in range(0,len(p),2)]
    print 'Chosen block:',p; i=0
    while True:    # nth block is padded using PKCS #5, and so modify (n-1)th block to find key length!
        p[i]='00'; data[-2]=''.join(p)
        print 'Modified block:',p,'\nPosition:',i+1
        if not test(''.join(data)): break
        sleep(1); i+=1
    disconnect(); print 'Last %d bytes are padded!'%(len(p)-i)
    return i            # Should return 5

def pad(File='CBC.txt',blocks=3,l=5):          # Automated brute-force process to find the stuff in padded block
    if l==None:
        if raw_input('Analyze padding (y/n)? ')=='y': l=analyze()
        else: return
    data=read(File,blocks); z=data[-1]; k=''.join(data[:-1])
    l=len(''.join(data[:-2]))/2+l; co=connect(); a={}
    if co==-1: print '\nConnection failed!'; return
    for j in range(l):
        p=len(k)/2-l+j; print 'Padding key: %s (%s)'%(p,format(p,'02x').upper())
        k=[int(k[i:i+2],16) if i<2*(l-j) else int(k[i:i+2],16)^p^(p+1) for i in range(0,len(k),2)]
        i=l-(j+1); t=k[i]; k[i]=0; sleep(3)
        while True:
            data[-2]=hexed(k); print 'Modified block:',data[-2]
            try: rc=test(''.join(data))
            except Exception: connect(); print 'Retrying...'; continue
            k[i]+=1
            if rc==1: k[i]-=1; a[i]=p^(t^k[i]); k=hexed(k); break
    disconnect(); m=len(data[-2])/2-l
    return [a[i] for i in a]+[m]*m      # Should give [94,47,35,60,46,11,11,11,11,11,11,11,11,11,11,11]
