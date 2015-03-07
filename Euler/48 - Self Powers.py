def self(n):
    s=0
    for i in range(1,n+1):
        s+=i**i
    return str(s)

#n=1000; r=10; print "The last " +str(r)+ " digits of the power series is: " +self(n)[-r:]
