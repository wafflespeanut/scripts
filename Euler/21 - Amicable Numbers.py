execfile("12 - Highly Divisible Triangular Number.py")

def d(n):
    s=0; f=factors(n)
    for i in f:
        if i!=n: s+=i
    return s

def amicables(n):
    coll=[]; s=0
    for i in range(2,n):
        a=d(i)
        if i==d(a): coll.append(a)
    for i in coll: s+=i
    return s

#n=10000; print "The sum of all amicable numbers under " +str(n)+ " is: " +str(amicables(n))
