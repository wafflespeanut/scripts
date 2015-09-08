from math import pi

points = [(0.285, 0.285), (1.425, 0.57), (1.425, 0.57),
          (2.185, 0.617), (3.23, 0.665), (4.18, 0.617),
          (5.13, 0.57), (6.175, 0.52), (6.65, 0.475),
          (6.65, 0.475), (7.41, 0.38), (8.17, 0.285),
          (9.025, 0.095), (8.075, -0.095), (6.65, -0.2375),
          (6.65, -0.2375), (6.08, -0.285), (4.75, -0.38),
          (3.42, -0.42), (2.28, -0.38), (1.425, -0.285),
          (1.425, -0.285), (0.475, -0.19)]

total = len(points)
stringer_area = 2.27741935e-3

spar_front = [1, 2, 20, 21]
spar_rear = [8, 9, 14, 15]

if 'stringer_area' in locals():
    A = [0.0004645 if i in spar_front else 0.0004 if i in spar_rear else stringer_area for i in range(total)]
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

for i in range(total):
    print i + 1, '\t\t', Ixx, '\t\t', Sigma[i] / 10 ** 6

print '\nLeast value of Ixx:', min(Ixx_)
print '\nMax value of Sigma:', max(map(abs, Sigma)) / 10 ** 6
print 'Critical Sigma:', ((pi ** 2) * 70e9 * min(Ixx_) / (stringer_area * 1.2 ** 2)) / 10 ** 6
print
