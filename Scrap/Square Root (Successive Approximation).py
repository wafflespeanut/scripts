def tr(int):
    def test(x):
        return 0.5*((int/x)+x)
    return test

def sqrtm1(int):
    def tr(x):
        return 0.5*((int/x)+x)
    def fixedPoint(f,epsilon):
        guess=1.0
        for i in range(100):
            if abs(f(guess)-guess)<epsilon: return guess
            else: guess=f(guess)
        return guess
    return fixedPoint(tr, 0.0001)

def sqrtm2(int):
    def fixedPoint(f,epsilon):
        guess=1.0
        for i in range(100):
            if abs(f(guess)-guess)<epsilon: return guess
            else: guess=f(guess)
        return guess
    return fixedPoint(tr(int),0.0001)
