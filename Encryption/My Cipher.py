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
    i=0;ph=len(phrase);p=len(key);hprime=hexed(str(primes))
    for j in pas:
        if i<=ph and primes[i]<ph:
            phrase=phrase[:primes[i]]+[j]+phrase[primes[i]:]
            i+=1
        else: break
    while phrase[-1]==None:
        phrase=phrase[:(len(phrase)-1)]
    return ''.join(phrase)

def bit(text,key,iteration):
    i=1;combined=combine(text,key)
    while i<=iteration:
        combined=combine(combined,key)
        i+=1
    return combined

print bit("abcd","encryp",5)
