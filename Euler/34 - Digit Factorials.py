execfile("15 - Lattice Paths.py")

def digitsFact(n):
    a=list(str(n)); s=0
    for i in a: s+=int(fact(int(i)))
    if s==n: return True
    else: return False

def sumdigits(r):
    curious=set()
    for i in range(r+1):
        if digitsFact(i) and i not in [1,2]: curious.update([i])
    return list(curious)

r=50000; s=sum(sumdigits(r))    # Another stupid guess!
print "The sum of all numbers which are equal to the sum of factorial of their digits is: " +str(s)
