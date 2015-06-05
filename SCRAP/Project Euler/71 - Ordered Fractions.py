execfile("5 - Smallest Multiple.py")

def frac(r,f):      # Brute-forcing! (Sucks for r>1000)
    def find(f): return float(f[0])/f[1]
    a=[1,r]; k=float(f[0])/f[1]
    for d in range(1,r+1):
        for n in range(1,d):
            if gcd(n,d)==1:
                if find([n,d])>find(a) and find([n,d])<k: a=[n,d]
    return a[0]

def num(r,f):     # Cheap algorithm for numerator!
    return int(round(f[0]*float(r)/f[1]-1))
        
#d=1000000; f=[3,7]; print "The numerator of the fraction immediately to the left of",f,"is:",num(d,f)
