execfile("7 - 10001st Prime.py")
from itertools import permutations

z=sieve(999999)

def ESieve(m,n): return [i for i in sieve(n) if i>m]

def perm(s):
    k=permutations(str(s)); a=[]
    for i in k: a.append(int(''.join(i)))
    return a

def isPrime(n):
    if n%2==0: return False
    for i in z:
        if n==i: return True
        if i>(n**0.5+1): break
        if n%i==0: return False
    return True

def gen(l,u):
    p=ESieve(l,u); a=[]
    for i in p:
        for j in p:
            if i<j:
                k=j+(j-i)
                if all([k<9999,isPrime(i),isPrime(j),isPrime(k)]):
                    m=perm(i)
                    if j in m and k in m: a.append([i,j,k])
    return a

#print "The other 4-digit sequence in which the terms are primes and permutations of one another is: "+str(gen(1489,6500)[0])
