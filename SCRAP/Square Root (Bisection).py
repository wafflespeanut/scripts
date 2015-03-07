def bisect(x):
    epsilon=0.01; n=0
    low=0.0; high=x; ans=(high+low)/2.0
    while abs(ans**2-x)>=epsilon:
        print("Lower bound: "+str(low)+ "\tHigher bound: "+str(high)+ "\tAnswer = " +str(ans))
        if ans**2<x: low=round(ans,5)
        else: high=round(ans,5)
        ans=(high+low)/2.0; n+=1
    print "\nGuessed " +str(n)+ " times!"
    return round(ans,5)

#x=49; print bisect(x)," is close to the square root of",str(x)+'!'
