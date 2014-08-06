def sqrt1(a):
    def tr(x):
        return 0.5*((a/x)+x)
    def fixedPoint(f,epsilon):
        guess=1.0
        for i in range(100):
            if abs(f(guess)-guess)<epsilon: return guess
            else: guess=f(guess)
        return guess
    return fixedPoint(tr, 0.0001)

def tr(a):
    def test(x):
        return 0.5*((a/x)+x)
    return test

def sqrt2(a):
    def fixedPoint(f,epsilon):
        guess=1.0
        for i in range(100):
            if abs(f(guess)-guess)<epsilon: return guess
            else: guess=f(guess)
        return guess
    return fixedPoint(tr(a),0.0001)
