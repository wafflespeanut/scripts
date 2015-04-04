execfile("Variant Vigenere.py")
from math import ceil
from os import path
from time import sleep

fin="CTEXT-2.txt"; key=[] # Key in hex byte strings

def xor(c1,c2):
    if not len(c1)==len(c2): return None
    for i in range(0,len(c1),2):
        m=hexor(c1[i:i+2],c2[i:i+2])
        print c1[i:i+2],'\t',c2[i:i+2],'\t',m,'\t',(8-len(bin(m)[2:]))*'0'+bin(m)[2:]

def ctexts():
    with open(fin,'r') as file: data=file.readlines()
    data=[i[:-1] if i[-1]=='\n' else i for i in data]
    return data
