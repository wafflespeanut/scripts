def factors(n):
    return set(reduce(list.__add__,([i,n/i] for i in range(1,int(n**0.5)+1) if not n%i)))

def tri(r): return r*(r+1)/2

def find(n):
    i=1
    while True:
        t=tri(i); f=len(factors(t))
        if f>=n: print("No: %i\tFactors: %s")%(t,f); break
        i+=1

#n=500; print "The first triangle number to have over " +str(n)+ " divisors..."; find(n)
