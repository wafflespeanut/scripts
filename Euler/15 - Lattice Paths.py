def fact(n):
    f=1
    for i in range(1,n+1): f*=i
    return f

def bino(m,n): return fact(m)/(fact(m-n)*fact(n))

# n=5
# print "There are " +str(bino(n*2,n))+ " routes through a " +str(n)+"x"+str(n)+ " grid!"
