def factors(n):
    return set(reduce(list.__add__,([i,n/i] for i in range(1,int(n**0.5)+1) if not n%i)))

def find(n):
    i=1
    while True:
        t=i*(i+1)/2; f=len(factors(t))
        if f>=n: print("No: %i\tFactors: %s")%(t,f); break
        i+=1
    return None

#n=500; print "The first triangle number to have over " +str(n)+ " divisors..."; find(n)
