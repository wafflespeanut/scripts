execfile("ADP - Airfoil Centroid.py")
from math import pi
import matplotlib.pyplot as plt

data = get_points("AIRFOIL.dat")

def stringers(nodes, dist_list, airfoil_data, sep):
    i, x, y, dist, resolved = 0, 0, 0, 0, []
    for node in nodes:
        while dist < node:
            (x0, y0), (x1, y1) = airfoil_data[i], airfoil_data[i + 1]
            delta = node - dist
            delta_x, delta_y = delta * (x1 - x0) / dist_list[i], delta * (y1 - y0) / dist_list[i]
            x, y = x0 + delta_x, y0 + delta_y
            dist += dist_list[i]
            i += 1
        if len(resolved) and resolved[-1] == (x, y):
            delta_x, delta_y = sep * (x1 - x0) / dist_list[i - 1], sep * (y1 - y0) / dist_list[i - 1]
            x, y = x + delta_x, y + delta_y
        resolved.append((x, y))
    return resolved

def form_stringers(chord = 9.5, stringers_top = 9, stringers_bottom = 6):
    def slope(p1, p2):
        try:
            return (p2[1] - p1[1]) / (p2[0] - p1[0])
        except ZeroDivisionError:
            return None

    split_index = [slope(data[i], data[i + 1]) for i in range(len(data) - 1)].index(None)
    airfoil_top, airfoil_bottom = data[:split_index + 1], data[split_index + 1:]

    def dist(p1, p2):
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    dist_top = [dist(airfoil_top[i], airfoil_top[i + 1]) for i in range(len(airfoil_top) - 1)]
    dist_bottom = [dist(airfoil_bottom[i], airfoil_bottom[i + 1]) for i in range(len(airfoil_bottom) - 1)]
    sep_top, sep_bottom = sum(dist_top) / (stringers_top + 1), sum(dist_bottom) / (stringers_bottom + 1)
    nodes_top = [sep_top * i for i in range(1, stringers_top + 1)]
    nodes_bottom = [sep_bottom * i for i in range(1, stringers_bottom + 1)]

    resolved_top = stringers(nodes_top, dist_top, airfoil_top, sep_top)
    resolved_bottom = stringers(nodes_bottom, dist_bottom, airfoil_bottom, sep_bottom)
    points = resolved_top + resolved_bottom
    st_x, st_y = zip(*points)
    plot_over_airfoil(data, st_x, st_y)
    flanges = []

    # while True:
    #     try:
    #         f = float(raw_input("Enter X-value of flange (in meters): "))
    #         flanges.append(f)
    #     except ValueError, KeyboardInterrupt:
    #         pass

    for i, point in enumerate(points):
        points[i] = str(point[0] * chord) + '\t' + str(point[1] * chord) + '\n'
    with open("STRINGERS.dat", 'w') as File:
        File.writelines(points)
    raw_input('Data has been written to STRINGERS.dat. Continue after adding flanges...')

def stringer_calc(chord = 9.5, stringer_area = 7e-3,
                  spar_front = [2, 18], spar_rear = [8, 14],
                  front_area = 0.0036946, rear_area = 0.0034003,
                  Sx = 11391789.36, Sy = 178265.8194):
    points = get_points("STRINGERS.dat")
    for i, point in enumerate(points):
        points[i] = point[0] / chord, point[1] / chord
    total = len(points)

    st_x, st_y = zip(*points)
    f_x, f_y = zip(*[point for i, point in enumerate(points) if (i + 1) in spar_front + spar_rear])

    if front_area and rear_area:
        A = [front_area if (i + 1) in spar_front
                       else rear_area if (i + 1) in spar_rear
                                      else stringer_area for i in range(total)]
    else:
        A = [stringer_area for i in range(total)]

    Ax = [A[i] * points[i][0] for i in range(total)]
    Ay = [A[i] * points[i][1] for i in range(total)]

    Xc, Yc = sum(Ax) / sum(A), sum(Ay) / sum(A)

    X_Xc = [points[i][0] - Xc for i in range(total)]
    Y_Yc = [points[i][1] - Yc for i in range(total)]

    Ixx_ = [A[i] * Y_Yc[i] ** 2 for i in range(total)]
    Iyy_ = [A[i] * X_Xc[i] ** 2 for i in range(total)]
    Ixy_ = [A[i] * X_Xc[i] * Y_Yc[i] for i in range(total)]

    Ixx = sum(Ixx_)
    Iyy = sum(Iyy_)
    Ixy = sum(Ixy_)

    Sigma = [((Ixy * Sx - Ixx * Sy) / (Ixx * Iyy - Ixy ** 2)) * (X_Xc)[i] +
            ((Ixy * Sy - Iyy * Sx) / (Ixx * Iyy - Ixy ** 2)) * (Y_Yc)[i] for i in range(total)]

    red, blue_1, blue_2, green, yellow, null = ('\033[' + str(i) + 'm' for i in (91, 96, 94, 92, 93, 0))

    print
    for i in range(total):
        a, b = blue_1, null
        if (i + 1) not in spar_front + spar_rear:
            a, b = '', ''
        print "  {}{}\t{}{}".format(a, i + 1, Sigma[i] / 10 ** 6, b)

    print '\n {}Least value of Ixx: {}{}\n'.format(blue_2, min(Ixx_), null)

    max_sigma = max(map(abs, Sigma)) / 10 ** 6
    critical_sigma = ((pi ** 2) * 70e9 * min(Ixx_) / (stringer_area * 1.4 ** 2)) / 10 ** 6

    color = red if max_sigma >= critical_sigma else green

    print ' {}Max value of Sigma: {} MPa{}'.format(color, max_sigma, null)
    print ' {}Critical Sigma: {} MPa{}'.format(yellow, critical_sigma, null)

    plot_over_airfoil(data, st_x, st_y, f_x, f_y)
