execfile("7 - 10001st Prime.py")
execfile("35 - Circular Primes.py")

def truncate(n):
    b=str(n); f=str(n); a=set([int(b)])
    while True:
        if b[:-1]!='': a.update([int(b[:-1])])
        else: break
        b=b[:-1]
    while True:
        if f[1:]!='': a.update([int(f[1:])])
        else: break
        f=f[1:]
    return a

def tprimes(r):
    primes=sieve(r); t=0; f=set([2])
    def check(a):
        for j in a:
            if int(j) not in primes: return False
        return True
    for i in primes:
        m=truncate(i); c=needs(i)
        if i<100: c=True
        if c and 1 not in m:
            if check(m): f.update([i])
    return list(sorted(f))[4:]

r=999999; s=sum(tprimes(r)); print "The sum of all 11 truncatable primes is: " +str(s)
