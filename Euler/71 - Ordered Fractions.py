execfile("5 - Smallest Multiple.py")

def find(r,f):
    def frac(f): return float(f[0])/f[1]
    a=[1,r]; k=float(f[0])/f[1]
    for d in range(1,r+1):
        for n in range(1,d):
            if gcd(n,d)==1:
                if frac([n,d])>frac(a) and frac([n,d])<k: a=[n,d]
    return a
