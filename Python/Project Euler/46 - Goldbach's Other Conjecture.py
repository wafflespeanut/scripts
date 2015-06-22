execfile("7 - 10001st Prime.py")

def goldbach(r):
    p=sieve(r); sq=[i*i for i in range(int(r**0.5+1))]
    def comp(r):
        c=[]
        for i in range(2,r+1):
            if i%2 and i not in p: c.append(i)
        return c
    com=comp(r); s=[True for i in range(len(com))]
    for i in range(len(com)):
        for j in p:
            if j<com[i] and (com[i]-j)/2 in sq: s[i]=False
    return [com[i] for i,j in enumerate(s) if j][0]

#r=6000; g=goldbach(r); print str(g)+ " falsifies Goldbach's conjecture!"
