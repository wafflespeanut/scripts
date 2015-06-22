execfile("5 - Smallest Multiple.py")

def triplet(r):
    t=[0]*(r+1)
    for m in range(1,int(r**0.5)):
        for n in range(1,m):
            if (m+n)%2 and gcd(m,n)==1:
                a=m**2-n**2; b=2*m*n; c=m**2+n**2
                p=a+b+c
            while p<=r: t[p]+=1; p+=(a+b+c)
    return t.count(1)

#r=1500000; print "There are {} values from which exactly one right angle triangle can be formed!".format(triplet(r))
