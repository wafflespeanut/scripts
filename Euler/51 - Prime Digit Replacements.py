execfile("49 - Prime Permutations.py")
import string
 
def check(p,r):
    c=0
    for i in '0123456789':
        n=int(string.replace(p,r,i))
        if(n>100000 and isPrime(n)): c+=1
    return c==8

def family(): 
    for i in ESieve(99999,999999):
        s=str(i); e=s[-1]
        if any([s.count('0')==3 and check(s,'0'),\
                s.count('1')==3 and e!= '1' and check(s,'1'),\
                s.count('2')==3 and check(s,'2')]): return s

#print "The eight prime family starts at " +family()
