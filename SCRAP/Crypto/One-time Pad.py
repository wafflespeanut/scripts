execfile("Variant Vigenere.py")
from math import ceil
from os import path
from time import sleep
from itertools import combinations as comb

fin="CTEXT-2.txt"; key=[] # Key in hex byte strings

def xor(c1,c2):
    if not len(c1)==len(c2): return None
    t1=[c1[i:i+2] for i in range(0,len(c1),2)]; t3=[]
    t2=[c2[i:i+2] for i in range(0,len(c2),2)]; t4=[]
    for i in range(len(t1)):
        p=str(hexor(t1[i],t2[i]))
        s=(' '+p if len(p)<2 else p); t3.append(s)
        t4.append(' '+chr(32^int(s)) if int(s)>40 else '  ')
    print '  '.join(t1),'\n','  '.join(t2),'\n','  '.join(t4)
##    for i in range(0,len(c1),2):
##        m=hexor(c1[i:i+2],c2[i:i+2]); x=(8-len(bin(m)[2:]))*'0'+bin(m)[2:]
##        s=('Space | Char' if x[:2]=='00' else 'Space & Char'); ch=''; k=''
##        if x=='0'*8: s='Same char!'
##        elif x[:2]=='01': ch=chr(m^32); k=i/2
##        print c1[i:i+2],'\t',c2[i:i+2],'\t',m,'\t',x,'\t',s,'\t',ch,'\t',k
    print '\n'; return None

def ctexts():
    with open(fin,'r') as file: data=file.readlines()
    data=[i[:-1] if i[-1]=='\n' else i for i in data]
    return (list(comb(data,2)),list(comb(range(len(data)),2)))

c=ctexts()[1]
for i,j in enumerate(ctexts()[0]):
    print 'M%s && M%s'%c[i]; xor(j[0],j[1])
