execfile("57 - Square Root Convergents.py")

def expand(n):
    t=0; d=1; a=int(n**0.5); s=[[a]]
    try:
        while a!=2*int(n**0.5):
            t=d*a-t
            d=(n-t**2)/d
            a=int((n**0.5+t)/d)
            s.append(a)
    except ZeroDivisionError: return None
    return s

def oddp(r):
    s=0
    for i in range(2,r+1):
        m=expand(i)
        if m and len(m)%2==0: s+=1
    return s

#r=10000; s=oddp(r); print "There are",s,'continued fractions having an odd period in the given range!'
