def fibo(n):
    i=-1; j=1; c=0; k=0
    while True:
        c=i+j; i=j; j=c; k+=1
        if len(str(c))==n: break
    return k-1

#n=1000; print "The first term in the Fibonacci series to contain " +str(n)+ " digits: " +str(fibo(1000))
