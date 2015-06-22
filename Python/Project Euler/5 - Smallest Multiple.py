def gcd(n1,n2): # Thanks to Euclid!
    t=0; a=n1; b=n2
    while b!=0: t=b; b=a%b; a=t
    return a

def lcm(a,b): return a*b/gcd(a,b)

def LCM(array):
    done=array[0]
    for i in array: done=lcm(done,i)
    return done

#n=20; li=range(1,n+1); print "The smallest number that's evenly divisible by first " +str(n)+ " numbers is: " +str(LCM(li))
