from math import pi

points = [(0.285, 0.285), (1.425, 0.57), (2.185, 0.617), (3.23, 0.665), (4.18, 0.617),
          (5.13, 0.57), (6.175, 0.52), (6.65, 0.475), (7.41, 0.38), (8.17, 0.285),
          (9.025, 0.095), (8.075, -0.095), (6.65, -0.2375), (6.08, -0.285), (4.75, -0.38),
          (3.42, -0.42), (2.28, -0.38), (1.425, -0.285), (0.475, -0.19)]

total = len(points)
stringer_area = 2.27741935e-3
spar_front, spar_rear = [1, 17], [7, 12]

if 'stringer_area' in locals():
    A = [0.0036946 if i in spar_front
                   else 0.0034003 if i in spar_rear
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

Sx, Sy = 11391789.36, 178265.8194
Sigma = [((Ixy * Sx - Ixx * Sy) / (Ixx * Iyy - Ixy ** 2)) * (X_Xc)[i] +
        ((Ixy * Sy - Iyy * Sx) / (Ixx * Iyy - Ixy ** 2)) * (Y_Yc)[i] for i in range(total)]

red, blue_1, blue_2, green, yellow, null = ('\033[' + str(i) + 'm' for i in (91, 96, 94, 92, 93, 0))

print
for i in range(total):
    a, b = blue_1, null
    if i not in spar_front + spar_rear:
        a, b = '', ''
    print "  {}{}\t{}{}".format(a, i + 1, Sigma[i] / 10 ** 6, b)

print '\n {}Least value of Ixx: {}{}\n'.format(blue_2, min(Ixx_), null)

max_sigma = max(map(abs, Sigma)) / 10 ** 6
critical_sigma = ((pi ** 2) * 70e9 * min(Ixx_) / (stringer_area * 1.4 ** 2)) / 10 ** 6

color = red if max_sigma >= critical_sigma else green

print ' {}Max value of Sigma: {} MPa{}'.format(color, max_sigma, null)
print ' {}Critical Sigma: {} MPa{}'.format(yellow, critical_sigma, null)
print
