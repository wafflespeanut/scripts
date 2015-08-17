import matplotlib.pyplot as plt

datapoints = [[0, 0], [3, 4], [6, 0]]     # an example triangle
# the vertices should be either clockwise or anticlockwise in direction (i.e., forming a loop)

# approximating airfoil as an irregular non-intersecting closed polygon (given by data points)
# let's now find the centroid: https://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

def get_points(file_name):
    with open(file_name, 'r') as File:
        stuff = File.readlines()
    datapoints = []
    for line in stuff:
        try:
            thing = line.split()
            point = float(thing[0]), float(thing[1])
        except ValueError:
            continue
        datapoints.append(point)
    return datapoints

def centroid(data = datapoints, ex = 0.1, ey = 0.05):
    if type(data) is str:
        data = get_points(data)
    def dry_helper(x0, x1, y0, y1):
        return x0 * y1 - y0 * x1
    num = len(data)
    data.append(data[0])
    x, y = zip(*data)
    area = sum(dry_helper(x[i], x[i+1], y[i], y[i+1]) for i in range(num)) / 2.0
    cx = sum((x[i] + x[i+1]) * dry_helper(x[i], x[i+1], y[i], y[i+1]) for i in range(num)) / (6 * area)
    cy = sum((y[i] + y[i+1]) * dry_helper(x[i], x[i+1], y[i], y[i+1]) for i in range(num)) / (6 * area)
    print '\nTotal area:', abs(area), '\n(X_c, Y_c) =', (cx, cy)

    plt.plot()
    ax = plt.gca()
    ax.set_xlim([min(x) - ex, max(x) + ex])
    ax.set_ylim([min(y) - ey, max(y) + ey])
    ax.set_aspect('equal')
    line = plt.plot(x, y)
    ax.figure.canvas.draw()
    ax.plot([cx], [cy], 'ob')
    plt.show()
