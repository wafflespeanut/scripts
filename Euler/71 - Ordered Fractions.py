execfile("5 - Smallest Multiple.py")

def HCF(f): g=gcd(f[0],f[1]); return [f[0]/g,f[1]/g]

def frac(f1,f2):
    if float(f1[0])/f1[1]>float(f2[0])/f2[1]: return 1
    elif float(f1[0])/f1[1]<float(f2[0])/f2[1]: return -1
    else: return 0

def fracgen(r):
    a=[]
    for n in range(1,r):
        for d in range(1,r+1):
            if gcd(n,d)==1: a.append([n,d])
    a.sort(frac)
    return a
