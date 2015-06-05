execfile("32 - Pandigital Products.py")

def genpans(n,r):
    cats=[]; pans=[]
    for i in range(1,r+1):
        k=1; s=''
        while len(s)<n:
            s+=str(i*k); k+=1
        if checkpan(n,s): pans.append([i,k-1]); cats.append(int(s))
    return [pans,cats]

#n=9; r=10000; pan=genpans(n,r)[-1][-1]      # Another stupid guess!
#print "The largest 1-9 pandigital number formed as a concatenated product of an integer with 1,2,...,n is: " +str(pan)
