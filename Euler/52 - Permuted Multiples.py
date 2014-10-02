execfile("49 - Prime Permutations.py")

def isPerm(s1,s2):
    a=str(s1); b=str(s2)
    if len(a)==len(b):
        for i in a:
            if a.count(i)!=b.count(i): return False
    else: return False
    return True

def multiperms(k,start,end):
    i=start; a=0; r=end/k[-1]
    while i<r:
        if isPerm(k[0]*i,i):
            c=0
            for j in k:
                if isPerm(i*j,i): c+=1
                else: break
            if c==len(k): a=i; break                    
        i+=1
    return a

#k=[2,3,4,5,6]; start=99999; end=999999; s=multiperms(k,start,end)
#print str(s)+ " is the smallest number divisible by " +str(k)+ " and all products are permutations of one another!"
