def fibonacci(n):
    s=0; i=-1; j=1; c=0
    while c<n:
        c=i+j; i=j; j=c
        if c%2==0: s+=c
    return s

#n=4000000; print "The sum of all even Fibonacci numbers upto " +str(n)+ " is: " + str(fibonacci(n))
