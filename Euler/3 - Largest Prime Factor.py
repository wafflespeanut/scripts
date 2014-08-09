execfile("7 - 10001st Prime.py")

n=600851475143

def evaluate(num):
    plist=sieve(100000); n=num; div=[] # Just a stupid guess!
    for i in plist:
        if int(n%i)==0:
            div.append(i)
    return max(div)

# print "The largest prime factor of " +str(n)+ " is: " +str(evaluate(n))
