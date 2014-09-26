execfile("49 - Prime Permutations.py")

def check(n1,n2): return isPrime(int(str(n1)+str(n2))) and isPrime(int(str(n2)+str(n1)))

def catable(p,r):   # returns an array of primes which might be a pair of the given prime!
    plist=[]
    for i in z:
        if i<r and check(i,p) and i!=p: plist.append(i)
        if i>r: break
    return plist

def able(n,arr):    # similar to catable(), but applies only to the given list
    l=[]
    for i in arr:
        if check(n,i) and i!=n: l.append(i)
    return l

def find():
    c=catable(13,10000); m=[]       # A ridiculous initialization based on a few trial & errors!
    for i in c:
        z=able(i,c); l=0
        while z: z=able(z[0],z); l+=1       # Trying to solve for at least one solution (got two!)
        m.append(l)
    k=max(m); l=[13]
    for i in range(len(m)):
        if m[i]==k: l.append(c[i])
    for i in c:
        if check(i,l[1]) and check(i,l[2]): l.append(i)
    return l

#s=find(); print sum(s),"is the lowest sum of five primes",s,"for which any prime pair concatenate to form another prime!"
