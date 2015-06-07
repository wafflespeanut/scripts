import timeit

def exhaust(n):                 # Brute-force method
    sidekick = []
    primes = []
    for i in range(2, n + 1):
        for j in range(2, int(n ** 0.5) + 1):
            if i * j not in sidekick and i * j <= n:
                sidekick.append(i * j)
        if i not in sidekick:
            primes.append(i)
    return primes

def lookup(n):                  # Half-assed sieve of Eratosthenes
    sidekick = []
    primes = []
    for i in range(2, n + 1):
        if i not in sidekick:
            primes.append(i)
            sidekick.extend(range(i * i, n + 1, i))
    return primes

def sieve(n):                   # Direct implementation of the sieve!
    sidekick = [False] * 2 + [True] * (n - 1)
    for i in range(int(n ** 0.5) + 1):
        if sidekick[i]:
            for j in range(i * i, n + 1, i):
                sidekick[j] = False
    return [j for j, prime in enumerate(sidekick) if prime]

r = 1000
print "Generating primes up to", str(r) + '...'
start = timeit.default_timer()
sieve(r)
stop = timeit.default_timer()
print "\tBoolean-marking took", round(stop - start, 5), "seconds"

start = timeit.default_timer()
lookup(r)
stop = timeit.default_timer()
print "\tList-looking took", round(stop - start, 5), "seconds"

start = timeit.default_timer()
exhaust(r)
stop = timeit.default_timer()
print "\tBrute-force took", round(stop - start, 5), "seconds"
