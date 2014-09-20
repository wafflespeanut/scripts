from itertools import product

def load(stuff):
    print "Loading names from file..."
    File=open(stuff,'r',0); List=''; a=[]; l=[]
    for i in File: List+=i
    for i in List.split(','): a.append(int(i))
    print "   ",len(a),"numbers loaded.\n"
    return a

def keygen(n):
    p=ord('a'); q=ord('z'); a=[]; l=[]
    for i in range(p,q+1): a.append(chr(i))
    for i in product(a,repeat=3): l.append(''.join(i))
    return l

def xorlist(p,k):
    l=[ord(i) for i in k]; m=[]; j=0
    for i in p:
        m.append(i^l[j]); j+=1
        if j==len(l): j=0
    return m

def find():
    l=keygen(3); k=[0,'']; p=a[:50]         # Took the first 50 chars to improve efficiency...
    for i in l:
        c=xorlist(p,i); s=c.count(32)       # Counting spaces - A crude assumption!
        if s>k[0]: k[0]=s; k[1]=i
    return k[1]

def count(k):
    p=xorlist(a,k); m=[]; s=0
    for i in p: s+=i
    return s

#a=load("CIPHER.txt"); k=find(); s=count(k); print "The sum of ASCII values of the plaintext is:",s
