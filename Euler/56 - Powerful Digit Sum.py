execfile("16 - Power Digit Sum.py")

def digital(a,b):
    s=[0]
    for i in range(2,a):
        for j in range(1,b):
            if sumup(i**j)>s[0]: s=[sumup(i**j),i,j]
    return s

#s=digital(100,100); print "The maximum digital sum is " +str(s[0])+ " obtained from " +str(s[1])+ "^" +str(s[2])+ "!"
