import string
import random

def sieve(n):
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [None]+[j for j,prime in enumerate(sidekick) if prime]
    
def cipher(key):
    pas=list(key)
    for i,j in enumerate(pas):
        pas[i]=hex(ord(pas[i]))[2:]
