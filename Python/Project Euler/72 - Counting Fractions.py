execfile("5 - Smallest Multiple.py")

def count(r):
    p=range(r+1); p[1]=0
    for n in range(2,r+1):
        if p[n]==n:
            for k in range(n,r+1,n): p[k]-=p[k]/n
    return sum(p)

#r=1000000; print "There are "+str(count(r))+" reduced proper fractions within "+str(r)+"!"
