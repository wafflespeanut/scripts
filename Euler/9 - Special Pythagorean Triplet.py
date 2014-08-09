def find(r):
    a=[]
    for i in range(1,r+1):
        for j in range(1,r+1):
            for k in range(1,r+1):
                if i**2+j**2==k**2: a.append([i,j,k])
    return a

def match(r,n):
    a=find(r)
    for i in a:
        if i[0]+i[1]+i[2]==n:
            return i

# exhaust=match(500,1000)
# print "The special Pythagorean triplet is " +str(exhaust)+ " whose product is " +str(exhaust[0]*exhaust[1]*exhaust[2])
