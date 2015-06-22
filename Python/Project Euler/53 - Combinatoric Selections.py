execfile("15 - Lattice Paths.py")

def count(r,c):
    a=0; i=1
    for n in range(i,r+1):
        for k in range(1,n):
            if bino(n,k)>c: a+=1
    return a

#r=100; c=10**6; s=count(r,c); print "There are " +str(s)+ " values exceeding " +str(c)+ " for 'n' in the range (1," +str(r)+')'
