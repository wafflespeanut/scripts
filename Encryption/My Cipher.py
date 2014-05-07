import string
from random import randrange

def sieve(n):
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [j for j,prime in enumerate(sidekick) if prime]
    
def hexed(key):
    pas=list(key)
    for i,j in enumerate(pas):
        pas[i]=format(ord(pas[i]),'02x')
    return pas

def combine(text,key):
    pas=hexed(key);phrase=hexed(text);primes=sieve(len(key)**2);
    i=0;ph=len(phrase);p=len(key)
    for j in pas:
        if primes[i]<len(phrase):
            phrase=phrase[:primes[i]]+[j]+phrase[primes[i]:]
            i+=1
        else: break
    return ''.join(phrase)

def char(key):
    pas=[key[i:i+2] for i in range(0,len(key),2)]
    for i,j in enumerate(pas):
        pas[i]=pas[i].decode("hex")
    return ''.join(pas)

def extract(text,key):
    phrase=char(text);primes=sieve(len(key)**2);
    ph=len(phrase);newph=""
    for i in range(ph):
        if i not in primes[:len(key)]:
            newph+=phrase[i]
    return newph

def ebit(text,key,iteration):
    i=1;combined=combine(text,key)
    while i<=iteration:
        combined=combine(combined,key)
        i+=1
    return combined

def dbit(text,key,iteration):
    i=1;extracted=extract(text,key)
    while i<=iteration:
        extracted=extract(extracted,key)
        i+=1
    return ''.join(extracted)

text=raw_input("Text to put in the cipher: ")
key=raw_input("Password: ")
level=raw_input("Security level (1-5): ")

what=raw_input("Encrypt (e) or Decrypt (d) ? ")
if str(what)=='e':
    e=ebit(str(text),str(key),int(level))
    print "\nENCRYPTED BITS: "+str(e)
elif str(what)=='d':
    d=dbit(str(text),str(key),int(level))
    print "\nDECRYPTED TEXT: "+str(d)
else: print "\nINVALID INPUT!"
