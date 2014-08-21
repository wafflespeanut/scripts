execfile("15 - Lattice Paths.py")

def factsum(n):
    f=str(fact(n)); s=0
    for i in f: s+=int(i)
    return s

#n=100; print "The sum of digits in " +str(n)+ "! is: " +str(factsum(n))
