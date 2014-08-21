def pals(n1,n2):
    a=[]; i=n2; j=n1
    while i>=n1:
        while j<=n2:
            t=str(i*j); j+=1
            if t==t[::-1]: a.append(int(t))
        i-=1; j=n1
    return list(set(a))

#print "The largest palindrome of the product of two 3-digit numbers: " +str(max(pals(100,999)))
