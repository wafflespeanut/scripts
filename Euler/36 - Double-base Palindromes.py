def palbases(r):
    a=0; b=0; pals=set()
    for i in range(r+1):
        a=str(i); b=bin(i)[2:]
        if a==a[::-1] and b==b[::-1]: pals.update([i])
    return pals

#r=1000000; s=sum(palbases(r)); print "The sum of all numbers (below 1 million) which are palindromic in base 2 and 10 is: " +str(s)
