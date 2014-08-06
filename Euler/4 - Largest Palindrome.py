a=[]; i=999; j=100; final=[]

while i>=100:
    while j<=999:
        t=str(i*j); j+=1
        if t==t[::-1]: a.append(int(t))
    i-=1; j=100

print "The largest palindrome of the product of two 3-digit numbers: " +str(max(a))
