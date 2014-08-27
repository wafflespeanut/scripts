def find(n):
    a=0; p=set()
    for b in range(1,n/2):
        a=(n*n/2-n*b)/(n-b); c=n-a-b
        if a**2+b**2==c**2: p.update([a,b,n-a-b])
    return list(p)

#n=1000; p=find(n); print "The special Pythagorean triplet is " +str(p)+ " whose product is: " +str(p[0]*p[1]*p[2])
