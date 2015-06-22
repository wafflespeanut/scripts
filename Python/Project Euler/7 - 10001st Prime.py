def sieve(n):
    '''Returns a list of primes using the sieve of Eratosthenes.'''
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i): sidekick[j]=False
    return [j for j,p in enumerate(sidekick) if p]

#print "10001st prime: " +str(sieve(1000000)[10000]) # Another stupid guess!