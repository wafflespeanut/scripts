def collatz(r):
    c={}; x=0; y=0
    for n in range(2,r+1):
        i=n; a=0
        while True:
            if i in c: c[n]=a+c[i]; break
            elif i==1: c[n]=a; break
            elif i%2==0: i=i/2; a+=1
            else: i=3*i+1; a+=1
        if c[n]>y: x=n; y=c[n]
    return (x,y+1)

#r=1000000; l=collatz(r); print "The longest chain in Collatz sequence is produced by",l[0],"-",l[1],"chains!"
