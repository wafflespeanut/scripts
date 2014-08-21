n1=3; n2=5; r=1000

def multiples(n1,n2,r):
    a=[]; s=0
    for i in range(r/min(n1,n2)+1):
        if n1*i<r: a+=[n1*i]
        if n2*i<r: a+=[n2*i]
    for i in list(set(a)): s+=i
    return s

#print 'The sum of multiples of ' +str(n1)+ ' "or" ' +str(n2)+ ' below ' +str(r)+ ': ' +str(multiples(n1,n2,r))
