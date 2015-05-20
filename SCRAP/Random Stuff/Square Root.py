def bisect(x):              # Bisection
    epsilon=0.01; n=0
    low=0.0; high=x; ans=(high+low)/2.0
    while abs(ans**2-x)>=epsilon:
        print("Lower bound: "+str(low)+ "\tHigher bound: "+str(high)+ "\tAnswer = " +str(ans))
        if ans**2<x: low=round(ans,5)
        else: high=round(ans,5)
        ans=(high+low)/2.0; n+=1
    print "\nGuessed",n,"times!"
    return round(ans,5)

def approx(i):                # Successive approximation
    def tr(x): return 0.5*((i/x)+x)
    def fixedPoint(f,epsilon):
        guess=1.0; z=0
        while True:
            if abs(f(guess)-guess)<epsilon: print '\nGuessed',z,'times!'; return guess
            else: guess=f(guess)
            z+=1; print "Guess:",round(guess,5)
        print '\nGuessed',z,'times!'
        return guess
    return fixedPoint(tr,0.0001)
