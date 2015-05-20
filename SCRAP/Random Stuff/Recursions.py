def maxi(seq):              # Find the largest number in a sequence
    if len(seq)==2:
        if seq[0]>seq[1]: return seq[0]
        else: return seq[1]
    return maxRecur([seq[0],maxRecur(seq[1:])])

def lace(s1,s2,out=''):           # Lace two strings
    if s1=='': return out+s2
    if s2=='': return out+s1
    else: return laceRecur(s1[1:],s2[1:],out+s1[0]+s2[0])
    return laceRecur(s1,s2)

def search(seq,n,i=0,l=None):       # Binary search through a sorted list
    if l==None: l=len(seq)-1
    if i==l: return l
    else:
        m=(i+l)/2
        if n>seq[m]: return search(seq,n,m+1,l)
        else: return search(seq,n,i,m)
