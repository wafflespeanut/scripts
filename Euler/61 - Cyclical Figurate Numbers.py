from itertools import permutations

def tri(n): return n*(n+1)/2
def sq(n): return n**2
def pen(n): return n*(3*n-1)/2
def hexa(n): return n*(2*n-1)
def hept(n): return n*(5*n-3)/2
def octa(n): return n*(3*n-2)

# INVERSE FUNCTIONS

def isTri(n): return int(((1+8*n)**0.5-1)/2)==((1+8*n)**0.5-1)/2
def isSq(n): return int(n**0.5)==n**0.5
def isPen(n): return int(((1+24*n)**0.5+1)/6)==((1+24*n)**0.5+1)/6
def isHex(n): return int(((1+8*n)**0.5+1)/4)==((1+8*n)**0.5+1)/4
def isHept(n): return int(((9+40*n)**0.5+3)/10)==((9+40*n)**0.5+3)/10
def isOct(n): return int(((1+3*n)**0.5+1)/3)==((1+3*n)**0.5+1)/3

def able(dad,son):
    a=[]
    def check(n1,n2): return str(n1)[:-3:-1][::-1]==str(n2)[:2]
    for i in dad:
        for j in son:
            if check(i,j) and j not in a: a.append(j)
    return a

def bunch(n):       # Generates lists of polygonal numbers
    def starts(f,r):
        i=1
        while True:
            if f(i)>=r: return i
            i+=1
    j=0; a=[]
    r1=[starts(i,10**(n-1)) for i in f]; r2=[starts(i,10**n)-1 for i in f]
    while j<len(f):
        b=[]
        for i in range(r1[j],r2[j]+1):
            m=f[j](i)
            if '0' in str(m):
                if str(m)[0]=='0' or str(m)[2]=='0': continue
                else: b.append(m)
            else: b.append(m)
        a.append(b); j+=1
    return a

def follow(p):      # Checks the properties for a given combination
    c=bunch(4); i=1; z=c[p[0]]; n=0
    while n<3:      # Just a funny assumption that no other combinations can survive after 3 iterations
        i=0; a=[]
        while i<len(p) and z:
            z=able(z,c[p[i]]); i+=1
            if z: a.append(z[0])
        n+=1
    if z: return a
    else: return False

def find():
    k=[]
    for i in p:
        if follow(i): return follow(i)
    return None

#f=[tri,sq,pen,hexa,hept,octa]; i=[i for i in range(len(f))]; p=list(permutations(i)); s=find()
#print "The sum of ordered set of",len(f),"cyclic 4-digit numbers is:",sum(s)
