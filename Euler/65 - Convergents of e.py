execfile("57 - Square Root Convergents.py")
execfile("16 - Power Digit Sum.py")

def exp(r):
    e=[1,1,2]; d=1
    while len(e)<=r:
        if (e[-1]+e[-2])%2==0: e.append(e[-1]+e[-2]+e[-3])
        else: e.append(d)
    e=e[1:-1]; f=frac(e[-2],d,d,e[-1]); e=e[:-2]
    while e: f=frac(e[-1],d,f[1],f[0]); e=e[:-1]
    return frac(2,1,f[1],f[0])

#n=100; f=exp(n); s=sumup(f[0]); print "The sum of digits in the numerator of",str(n)+'th convergent is:',s
