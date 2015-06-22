def d(n):
    s=""; i=1
    while len(s)<=n: s+=str(i); i+=1
    return int(s[n-1])

#s=d(1)*d(10)*d(100)*d(1000)*d(10000)*d(100000)*d(1000000)
#print "The product of those fractional parts in the concatenated irrational decimal fraction is: " +str(s)
