def farey(r,f1,f2):
    a=f1[0]; b=f1[1]; t=0
    if r%f1[1]: c=r/f1[1]+1; d=r
    else: c=r/f1[1]; d=r-1
    while c!=f2[0] and d!=f2[1]:
        k=(r+b)/d; e=k*c-a; f=k*d-b
        a=c; b=d; c=e; d=f
        t+=1
    return t

#r=12000; f1=[1,3]; f2=[1,2]; f=farey(r,f1,f2)
#print "For 'd' up to {}, there are {} fractions lying between {}/{} and {}/{}!".format(r,f,f1[0],f1[1],f2[0],f2[1])
