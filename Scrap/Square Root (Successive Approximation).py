def sqrt(i):
    def tr(x): return 0.5*((i/x)+x)
    def fixedPoint(f,epsilon):
        guess=1.0
        for i in range(100):
            if abs(f(guess)-guess)<epsilon: return guess
            else: guess=f(guess)
        return guess
    return fixedPoint(tr,0.0001)
