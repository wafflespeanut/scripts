n=600851475143

def sieve(n):
    sidekick=[0]*2+[1]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j]=0
    return [j for j,p in enumerate(sidekick) if p]

def evaluate(num):
    plist=sieve(100000); n=num; div=[] # just a stupid guess!
    for i in plist:
        if int(n%i)==0:
            div.append(i)
    return max(div)

print "The largest prime factor of " +str(n)+ " is: " +str(evaluate(n))
