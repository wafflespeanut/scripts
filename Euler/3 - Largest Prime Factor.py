execfile("7 - 10001st Prime.py")

plist=sieve(10000)

def evaluate(num):
    n=num; div=[]  # Just a stupid guess!
    for i in plist:
        if int(n%i)==0:
            div.append(i)
    return max(div)

#n=600851475143; print "The largest prime factor of " +str(n)+ " is: " +str(evaluate(n))
