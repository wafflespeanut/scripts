from itertools import combinations

def sets(n):        # Gives the possible sets for working out by hand!
    def check(l):
        c=0
        for i in l:
            if i>n: c+=1
        if c>1: return False
        return True
    l=range(1,n*2+1); s=(2*sum(l[:n])+sum(l[n:]))/n
    c=list(combinations(l,3))
    a=[list(i) for i in c if sum(i)==s and check(i)]
    return a

def couple(l):
    s=''
    for i in l:
        for j in i: s+=str(j)
    return s

#s=[[6,5,3],[10,3,1],[9,1,4],[8,4,2],[7,2,5]]   # After matching stuff in paper!
#print "The maximum 16-digit string is:",couple(s)
