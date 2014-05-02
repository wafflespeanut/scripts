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

def arraylook(n):
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [j for j,prime in enumerate(sidekick) if prime]

start=timeit.default_timer()
arraylook(1200)
stop=timeit.default_timer()
print "Array-looking took " +str(stop-start) +" seconds"

start=timeit.default_timer()
listlook(1200)
stop=timeit.default_timer()
print "List-looking took " +str(stop-start) +" seconds"

start=timeit.default_timer()
exhausted(1200)
stop=timeit.default_timer()
print "Brute-force took " +str(stop-start)+ " seconds"
