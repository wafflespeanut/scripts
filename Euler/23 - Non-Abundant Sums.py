execfile("12 - Highly Divisible Triangular Number.py")
limit=28123

def ab(n):
    f=factors(n); s=0
    for i in f:
        if i!=n: s+=i
    return s>n

def abuns(): return [x for x in range(1,limit+1) if ab(x)]

def absum(ablist,n):
    for i in ablist:
        if i>n: return False
        if (n-i) in ablist: return True
    return False

def nonabsum():
    ablist=set(abuns()); s=0    # set() has a nice structure compared to list
    nonab=[i for i in range(1,limit+1) if not absum(ablist,i)]
    for i in nonab: s+=i
    return s

#print "The sum of all positive integers which cannot be written as the sum of two abundant numbers is: " +str(nonabsum())
