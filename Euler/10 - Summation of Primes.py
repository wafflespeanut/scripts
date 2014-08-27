execfile("7 - 10001st Prime.py")

def tosum(n):
    s=0
    for i in sieve(n): s+=i
    return s

#print "The sum of all primes below 2 million: " +str(tosum(2000000))
