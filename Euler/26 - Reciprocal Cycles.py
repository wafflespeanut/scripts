execfile("7 - 10001st Prime.py")

def primes(n): return [3]+sieve(n)[3:]

def recur(n,i):
    for k in range(1,i):
        if 1==10**k %i: return k
    return 0

def maxreci(n,r):
    plist=primes(r); t=0; final=[]
    for i in plist:
        if recur(n,i)>t: t=recur(n,i); final=[i,t]
    return final

#n=1; r=1000; t=maxreci(n,r)
#print "The value which contains the longest recurring cycle in unit fractions is: " +str(t[0])+ " (" +str(t[1])+ " numbers recurred)"
