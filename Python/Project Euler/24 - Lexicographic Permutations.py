from itertools import permutations

def perm(li,n):
    a=list(permutations(li))
    return ''.join(list(a[n-1]))

#n=1000000; l="0123456789"; print "The millionth lexicographic permutation of the given range is: " +str(perm(l,n))
