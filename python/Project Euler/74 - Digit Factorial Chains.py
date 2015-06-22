d=[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

def fsum(n):
    s=0
    while n!=0: s+=d[n%10]; n/=10
    return s

def chains(r,p):
    c={}; m=0
    c[0]=1; c[1]=1; c[2]=1; c[145]=1
    for n in range(r+1):
        s=fsum(n); a=[n]; k=0
        while True:
            if n in c: break
            if s in c: k=len(a)+c[s]; c[n]=k; break
            a.append(s); s=fsum(s)
            if s in a or s==n: k=len(a); c[n]=k; break
        if c[n]==p: m+=1
    return m

#r=1000000; n=60; c=chains(r,n); print "There are",c,"chains with",n,"terms!"
