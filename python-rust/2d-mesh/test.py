import matplotlib.pyplot as plt

image = "target/image.png"
dataFile = "target/sample"              # Rust's input sample (for testing)

def generate(xmax = 1, ymax = 1):       # draw a closed structure
    plt.plot()
    ax = plt.gca()
    ax.set_xlim([0, xmax])
    ax.set_ylim([0, ymax])
    img = plt.imread(image)
    ax.imshow(img, extent = [0, xmax, 0, ymax], aspect = 'auto')
    points = plt.ginput(0)
    while intersectionExists(points):
        points = plt.ginput(0)
    points.append(points[0])            # form a closed structure
    x, y = zip(*points)
    line = plt.plot(x, y)
    ax.figure.canvas.draw()
    data = [str(x) + '\t' + str(y) for x, y in points]
    with open(dataFile, 'w') as file:
        file.writelines('\n'.join(data))

def intersectionExists(points):         # check whether points intersect in a list of point tuples
    if not points:
        print 'No input! Try again...'
        return True
    i, j = 0, 0
    while i < len(points) - 1:
        line1 = points[i], points[i+1]
        j = i + 2
        while j < len(points) - 1:
            line2 = points[j], points[j+1]
            if intersects(line1, line2):
                print 'Line intersection detected! Try again...'
                return True
            j += 1
        i += 2
    return False

def approxEqual(a, b, tol = 1e-10):     # check the difference within a tolerance instead of a direct equality
    return abs(a - b) <= tol

def intersects(line1, line2, point = False):
    # using Cramer's rule for the parametric forms, with 0 <= (s, t) <= 1
    # l1(t) = (x1, y1)*(1-t) + (x2, y2)*t
    # l2(s) = (u1, v1)*(1-s) + (u2, v2)*s
    (x1, y1), (x2, y2) = line1
    (u1, v1), (u2, v2) = line2
    (a, b), (c, d), (e, f) = (x2 - x1, u1 - u2), (y2 - y1, v1 - v2), (u1 - x1, v1 - y1)
    det = float(a * d - b * c)
    if approxEqual(det, 0):         # the lines don't intersect! there's no solution!
        if point:
            if approxEqual(float(e) / b, float(f) / d):     # collinear points
                return x1, y1       # (when t = 0 and s = e/b or f/d)
        return False
    else:                           # an unique solution corresponding to intersection
        t = (e * d - b * f) / det
        if point:
            return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        s = (a * f - e * c) / det
        return 0 <= t <= 1 and 0 <= s <= 1
