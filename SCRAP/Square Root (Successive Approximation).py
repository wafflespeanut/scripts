def sqrt(i):
    def tr(x): return 0.5*((i/x)+x)
    def fixedPoint(f,epsilon):
        guess=1.0; z=0
        for i in range(100):
            if abs(f(guess)-guess)<epsilon: return guess
            else: guess=f(guess)
            z+=1; print "Guess:",round(guess,5)
        print 'Guessed',z,'times!\n'
        return guess
    return fixedPoint(tr,0.0001)

#x=49; s=sqrt(x); print '\n',s,"is close to the square root of",str(x)+'!'
