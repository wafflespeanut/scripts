execfile("49 - Prime Permutations.py")

def pspiral(f):         # Problem-28 re-engineered!
    c=1; s=0; i=1; d=1
    while True:
        r=1
        while r<=4:
            if c%2==1:
                i+=c+1; d+=1
                if isPrime(i): s+=1
            r+=1
        c+=1
        if round(float(100)*s/d,4)<f: return c+1
    return None

#f=10; l=pspiral(f); print "The side length of square spiral for which the ratio of primes fall below " +str(f)+ "% is: " +str(l)
