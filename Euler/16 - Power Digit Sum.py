def power(num,n):
    bi=str(num**n); s=0
    for i in bi: s+=int(i)
    return s

#num=2; n=1000; print "The sum of digits of " +str(num)+ "^" +str(n)+ ": " +str(power(num,n))
