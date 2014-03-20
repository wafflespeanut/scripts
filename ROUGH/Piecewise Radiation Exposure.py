import math
def f(x):
    return 10*math.e**(math.log(0.5)/5.27 * x)

def radexp(st,sp,s):
    count=0
    i=st
    while i<sp:
        count+=(f(i)*s)
        i+=s
    return count
