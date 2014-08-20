execfile("15 - Lattice Paths.py")

n=100; f=str(fact(n)); s=0
for i in f:
    s+=int(i)

print "The sum of digits in " +str(n)+ "! is: " +str(s)
