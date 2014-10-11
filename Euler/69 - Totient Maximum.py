execfile("5 - Smallest Multiple.py")
execfile("49 - Prime Permutations.py")

def totient(n):
    if n in z: return n-1
    return len([i for i in range(1,n+1) if gcd(i,n)==1])

def maxi(r):        # The maximum occurs when multiplying primes!
    t=1; i=0; c=0
    while t<=r: c=t; t*=z[i]; i+=1
    return (c,totient(c),float(c)/totient(c))

#r=1000000; s=maxi(r); print "The maximum occurs at n={}! (Totient: {}, Ratio: {})".format(*s)
