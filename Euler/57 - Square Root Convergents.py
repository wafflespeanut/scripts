execfile("5 - Smallest Multiple.py")

def frac(n1,d1,n2,d2):
    d=lcm(d1,d2); n=(n1*d)/d1+(n2*d)/d2
    return [n,d]

def expand(i):
    s=[2,1]
    for i in range(i):
        s=frac(2,1,s[1],s[0])
    s=frac(1,1,s[1],s[0])
    return s

def find(r):
    s=0
    for i in range(r+1):
        m=expand(i)
        if len(str(m[0]))>len(str(m[1])): s+=1
    return s

#r=1000; m=find(r); print "In the first " +str(r)+ " expansions, there are " +str(m)+ " fractions where numerators have more digits than the denominator!"
