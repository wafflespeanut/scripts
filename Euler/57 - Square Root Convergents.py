execfile("5 - Smallest Multiple.py")

def frac(n1,d1,n2,d2):
    if n2==1 and type(d2)==list and len(d2)==2: n2=n2*d2[1]; d2=d2[0]
    elif n1==1 and type(d1)==list and len(d1)==2: n1=n1*d1[1]; d1=d1[0]
    d=lcm(d1,d2); n=(n1*d)/d1+(n2*d)/d2
    return [n,d]

def expand(r):
    s=[2,1]; i=1; c=0
    while i<r:
        s=frac(2,1,s[1],s[0]); i+=1
        m=frac(1,1,s[1],s[0])
        if len(str(m[0]))>len(str(m[1])): c+=1
    return c

#r=1000; m=expand(r); print "In the first " +str(r)+ " expansions, there are " +str(m)+ " fractions where numerators have more digits than the denominator!"
