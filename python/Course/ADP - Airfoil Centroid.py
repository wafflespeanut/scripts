data = []
# the vertices should be either clockwise or anticlockwise in direction (i.e., forming a loop)
data = [[0, 0], [3, 4], [6, 0]]     # for a triangle

# Let's approximate this as an irregular non-intersecting closed polygon
# https://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

def centroid(data):
    def dry_helper(x0, x1, y0, y1):
        return x0 * y1 - y0 * x1
    num = len(data)
    data.append(data[0])
    x, y = zip(*data)
    area = sum(dry_helper(x[i], x[i+1], y[i], y[i+1]) for i in range(num)) / 2.0
    cx = sum((x[i] + x[i+1]) * dry_helper(x[i], x[i+1], y[i], y[i+1]) for i in range(num)) / (6 * area)
    cy = sum((y[i] + y[i+1]) * dry_helper(x[i], x[i+1], y[i], y[i+1]) for i in range(num)) / (6 * area)
    print '\nTotal area:', abs(area), '\n(X_c, Y_c) =', (cx, cy)
    return (cx, cy)
