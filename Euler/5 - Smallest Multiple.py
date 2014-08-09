execfile("7 - 10001st Prime.py")

def gcd(n1,n2): # Thanks to Euclid!
    t=0; a=n1; b=n2
    while b!=0:
        t=b; b=a%b; a=t
    return a

def lcm(a,b):
    return a*b/gcd(a,b)

def LCM(array):
    done=array[0]
    for i in array:
        done=lcm(done,i)
    return done

li=[i for i in range(1,21)]

# print "The smallest number that's evenly divisible by first 20 numbers is: " +str(LCM(li))
