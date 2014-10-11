def center(n):
    s=(n**2)*((n**2)+1)/2; return s/(n**2)

def square(n):
    a=[[0 for i in range(n)] for i in range(n)]; c=2
    def roll(i):
        if i==len(a): return i-len(a)
        else: return i
    i=len(a)-1; j=len(a)/2; a[i][j]=1; a[j][j]=center(n)
    while c<=n**2:
        i+=1; j+=1
        i=roll(i); j=roll(j)
        if a[i][j]==c: continue
        if a[i][j]: i-=2; j-=1
        if c==center(n): c+=1
        a[i][j]=c; c+=1
    return a

def magic(n):
    a=square(n)
    for i in a: print '\t'.join([str(j) for j in i])
    return None
