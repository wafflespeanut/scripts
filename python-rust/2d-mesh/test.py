import matplotlib.pyplot as plt

def generate():
    plt.plot()
    ax = plt.gca()
    ax.set_xlim([0, 5])
    ax.set_ylim([0, 5])
    points = plt.ginput(0)
    x, y = zip(*points)
    line = plt.plot(x,y)
    ax.figure.canvas.draw()
    return points

# assert 5.5001 - 5.0 != 0.5001                 # shit happens!
# assert approxEqual(5.5001 - 5.0, 0.5001)      # works now!
# because, one can't check the equality of two floats, due to the erroneous internal representation of floats

def approxEqual(a, b, tol = 1e-10):         # check the actual difference with the allowable relative difference
    return abs(a - b) <= tol

def intersects(line1, line2, point = False):
    # using Cramer's rule for the parametric forms,
    # l(t) = (x1, y1)*(1-t) + (x2, y2)*t
    # j(t) = (u1, v1)*(1-s) + (u2, v2)*s
    (x1, y1), (x2, y2) = line1
    (u1, v1), (u2, v2) = line2
    (a, b), (c, d), (e, f) = (x2 - x1, u1 - u2), (y2 - y1, v1 - v2), (u1 - x1, v1 - y1)
    det = float(a * d - b * c)
    if approxEqual(det, 0):
        # the lines don't intersect! there's no solution!
        if point:
            if approxEqual(float(e) / b, float(f) / d):        # collinear (when t=0 and )
                return x1, y1
        return False
    else:
        t = (e * d - b * f) / det
        if point:
            return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        s = (a * f - e * c) / det
        # there should be an unique solution corresponding to intersection
        return 0 <= t <= 1 and 0 <= s <= 1

line1 = ((4, 4), (10, 10))
line2 = ((11, 5), (5, 11))
line3 = ((11, 5), (9, 7))

assert intersects(line1, line2) == True
assert intersects(line2, line3) == False
