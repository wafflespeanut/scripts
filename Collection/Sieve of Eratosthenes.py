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

start=timeit.default_timer()
listlook(300)
stop=timeit.default_timer()
print "List-looking took " +str(stop-start) +" seconds"

start=timeit.default_timer()
exhausted(300)
stop=timeit.default_timer()
print "Brute-force took " +str(stop-start)+ " seconds"
