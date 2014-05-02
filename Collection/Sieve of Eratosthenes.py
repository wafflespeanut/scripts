import timeit

def exhausted(n):
    sidekick=[]
    primes=[]
    for i in range(2,n+1):
        for j in range(2,n+1):
            sidekick.append(i*j)
        if i not in sidekick:
            primes.append(i)

def listlook(n):
    sidekick=[]
    primes=[]
    for i in range(2,n+1):
        if i not in sidekick:
            primes.append(i)
            sidekick.extend(range(i*i,n+1,i))

def arraylook(limit):
    sidekick=[False]*2+[True]*(limit-1) 
    for n in range(int(limit**0.5+1.5)):
        if sidekick[n]:
            for i in range(n*n,limit+1,n):
                sidekick[i] = False
    return [i for i, prime in enumerate(sidekick) if prime]

start=timeit.default_timer()
arraylook(300)
stop=timeit.default_timer()
print "Array-looking took " +str(stop-start) +" seconds"

start=timeit.default_timer()
listlook(300)
stop=timeit.default_timer()
print "List-looking took " +str(stop-start) +" seconds"

start=timeit.default_timer()
exhausted(300)
stop=timeit.default_timer()
print "Brute-force took " +str(stop-start)+ " seconds"
