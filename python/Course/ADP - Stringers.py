execfile("ADP - Airfoil Centroid.py")
from math import pi
import matplotlib.pyplot as plt

out = "STRINGERS.dat"
data = get_points("AIRFOIL.dat")        # airfoil data obtained from http://airfoiltools.com/
red, blue_1, blue_2, green, yellow, null = ('\033[' + str(i) + 'm' for i in (91, 96, 94, 92, 93, 0))

chord = 9.5
flanges = [1.425, 6.65]
stringers_top, stringers_bottom = 9, 6
stringer_area = 1.16 / 1550
front_area, rear_area = 11.462e-4, 9.8338e-4
Sx, Sy = 28479473.4, 2847947.34

def stringers(nodes, dist_list, airfoil_data, sep):
    i, dist, resolved = 0, 0, []
    for node in nodes:          # join every two points to form a right triangle (relative to the horizontal)
        while dist < node:      # iterate over the points to find the co-ordinates by resolving individual triangles
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

def form_stringers(n_top = stringers_top, n_bottom = stringers_bottom, distance_required = False):
    def slope(p1, p2):
        try:
            return (p2[1] - p1[1]) / (p2[0] - p1[0])
        except ZeroDivisionError:       # slope's undefined for a vertical line
            return None                 # which is how we're splitting the airfoil data

    split_index = [slope(data[i], data[i + 1]) for i in range(len(data) - 1)].index(None)
    airfoil_top, airfoil_bottom = data[:split_index + 1], data[split_index + 1:]

    def dist(p1, p2):
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    # generate the lengths of line segments
    dist_top = [dist(airfoil_top[i], airfoil_top[i + 1]) for i in range(len(airfoil_top) - 1)]
    dist_bottom = [dist(airfoil_bottom[i], airfoil_bottom[i + 1]) for i in range(len(airfoil_bottom) - 1)]
    # find the separation for placing the given stringers
    sep_top, sep_bottom = sum(dist_top) / (n_top + 1), sum(dist_bottom) / (n_bottom + 1)
    print '\n Spacing at the top (m):', sep_top * chord, '\n Spacing at the bottom (m):', sep_bottom * chord
    # generate the equidistant positions for stringers along the curve of the airfoil
    nodes_top = [sep_top * i for i in range(1, n_top + 1)]
    nodes_bottom = [sep_bottom * i for i in range(1, n_bottom + 1)]
    # resolve the points from the curve to the horizontal to find their absolute position
    resolved_top = stringers(nodes_top, dist_top, airfoil_top, sep_top)
    resolved_bottom = stringers(nodes_bottom, dist_bottom, airfoil_bottom, sep_bottom)

    def collinear_points(start_point, end_point, middle):
        (x1, y1), (x2, y2), (x0, y0) = start_point, end_point, middle
        try:
            return round((x0 - x1) / (x2 - x1), 6) == round((y0 - y1) / (y2 - y1), 6)
        except ZeroDivisionError:
            return False

    def compare_dist(list_to_check, generated_list):    # to find the inter-stringer distance except behind the rear spar
        generated_list = map(lambda point: (point[0] * chord, point[1] * chord), generated_list)
        i, j, dist_list = 0, 0, []          # Scale everything up!
        while i < len(list_to_check) - 1:
            total_dist = 0
            while j < len(generated_list) - 1 and \
                  'FLANGE' not in list_to_check[i] and \
                  not collinear_points(generated_list[j], generated_list[j + 1], list_to_check[i]):
                total_dist += dist(generated_list[i], generated_list[i + 1])
                j += 1
            if 'FLANGE' in list_to_check[i]:
                dist_list.append(dist(list_to_check[i], list_to_check[i + 1]))
            elif total_dist:
                dist_list.append(total_dist)
            i += 1
        return dist_list

    if distance_required:
        split_index = 0
        st_data = get_points(out, 'FLANGE')
        for i, point in enumerate(data):
            if point[1] < 0:
                split_index = i
                break
        print compare_dist([(0, 0)] + st_data[:split_index], [(0, 0)] + resolved_top)
        return None

    def find_y(x, p1, p2):              # find `y` for a given `x` lying on the line joining two points
        (x0, y0), (x1, y1) = p1, p2
        dx, dy = x1 - x0, y1 - y0
        return y0 + (x - x0) * (dy / dx)        # just a simplified form of sines & cosines

    def insert_flanges(top, bottom):
        i, j = 0, n_bottom - 1
        for fx in flanges:      # insert the stuff simultaneously to avoid unwanted complication
            fx = fx / chord
            while fx > top[i][0]:
                i += 1
            fy = find_y(fx, top[i - 1], top[i])
            top.insert(i, (fx, fy, 'FLANGE'))
            while fx > bottom[j][0]:
                j -= 1
            fy = find_y(fx, bottom[j + 1], bottom[j])
            bottom.insert(j + 1, (fx, fy, 'FLANGE'))

    insert_flanges(resolved_top, resolved_bottom)
    points = resolved_top + resolved_bottom
    for i, point in enumerate(points):
        f = 'FLANGE' if 'FLANGE' in point else ''        # just to differentiate the flanges for later use
        points[i] = str(point[0] * chord) + '\t' + str(point[1] * chord) + '\t\t' + f + '\n'     # scale up
    with open(out, 'w') as File:
        File.writelines(points)
    raw_input('\n {}NOTE:{} Data has been written to "{}"! Continue after checking the flanges...\n'.format(yellow, null, out))
    stringer_calc()

def stringer_calc():
    flange_pos, spar_front, spar_rear = [], [], []
    points = get_points("STRINGERS.dat", 'FLANGE')
    total = len(points)

    scaled_points = points[:]
    for i, point in enumerate(scaled_points):
        scaled_points[i] = point[0] / chord, point[1] / chord   # scale down (back to original values for plotting)
        if 'FLANGE' in point:
            flange_pos.append(i)

    spar_front.extend([flange_pos[0], flange_pos[-1]])
    spar_rear.extend([flange_pos[1], flange_pos[-2]])

    st_x, st_y = zip(*scaled_points)
    f_x, f_y = zip(*[point for i, point in enumerate(scaled_points) if i in spar_front + spar_rear])

    if front_area and rear_area:
        A = [front_area if i in spar_front
                       else rear_area if i in spar_rear
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

    Ixx, Iyy, Ixy = sum(Ixx_), sum(Iyy_), sum(Ixy_)

    Sigma = [((Ixy * Sx - Ixx * Sy) / (Ixx * Iyy - Ixy ** 2)) * (X_Xc)[i] +
            ((Ixy * Sy - Iyy * Sx) / (Ixx * Iyy - Ixy ** 2)) * (Y_Yc)[i] for i in range(total)]

    for i in range(total):
        a, b = blue_1, null
        if i not in spar_front + spar_rear:
            a, b = '', ''
        print "\t{}{}\t{}\t{}{}".format(a, i + 1, Ixx_[i], Sigma[i] / 10 ** 6, b)

    max_sigma = max(map(abs, Sigma)) / 10 ** 6
    critical_sigma = ((pi ** 2) * 150e9 * min(Ixx_) / (stringer_area * 1.4 ** 2)) / 10 ** 6
    color = red if max_sigma >= critical_sigma else green

    print '\n {}Least value of Ixx: {}{}\n'.format(blue_2, min(Ixx_), null)
    print ' {}Maximum Stress: {} MPa{}'.format(color, max_sigma, null)
    print ' {}Critical Stress: {} MPa{}'.format(yellow, critical_sigma, null)
    plot_over_airfoil(data, st_x, st_y, f_x, f_y)

while True:
    try:
        something = raw_input('\nContinue after making changes. You can...\n\n\
        1. [Enter] to continue with stringer calculation...\n\
        2. Regenerate, by entering the values for the number of stringers (both top and bottom) and [Enter]...\n\
        4. Ctrl-C to quit!\n')
        if something == '':
            form_stringers(500, 500, True)    # Meshing based on the airfoil data, just to ensure approximation
            stringer_calc()
        else:
            try:
                s = something.split()
                form_stringers(int(s[0]), int(s[1]))
            except (ValueError, IndexError):
                print '\n{}[ERROR]{} Cannot parse the value! Going back to old values...'.format(red, null)
                form_stringers()
    except KeyboardInterrupt:
        break
