points = [(0.285, 0.285), (1.425, 0.57), (1.425, 0.57),
          (2.185, 0.617), (3.23, 0.665), (4.18, 0.617),
          (5.13, 0.57), (6.175, 0.52), (6.65, 0.475),
          (6.65, 0.475), (7.41, 0.38), (8.17, 0.285),
          (9.025, 0.095), (8.075, -0.095), (6.65, -0.2375),
          (6.65, -0.2375), (6.08, -0.285), (4.75, -0.38),
          (3.42, -0.42), (2.28, -0.38), (1.425, -0.285),
          (1.425, -0.285), (0.475, -0.19)]

total = len(points)
constant_stingers = [1, 2, 8, 9, 14, 15, 20, 21]
initial_area = [0.000748 for i in range(total)]

A = [2.58e-03 if i not in constant_stingers else initial_area[i] for i in range(total)]

Ax = [A[i] * points[i][0] for i in range(total)]
Ay = [A[i] * points[i][1] for i in range(total)]

Ixx = [Ay[i] * points[i][1] for i in range(total)]
Iyy = [Ax[i] * points[i][0] for i in range(total)]
Ixy = [Ax[i] * points[i][1] for i in range(total)]

Xc, Yc = sum(Ax) / sum(A), sum(Ay) / sum(A)

X_Xc = [points[i][0] - Xc for i in range(total)]
Y_Yc = [points[i][1] - Yc for i in range(total)]

Sx, Sy = 744413.5006, 8448.1
Sigma = [((Ixy[i] * Sx - Ixx[i] * Sy) / (Ixx[i] * Iyy[i] - Ixy[i])) * (X_Xc)[i] +
        ((Ixy[i] * Sy - Ixx[i] * Sx) / (Ixx[i] * Iyy[i] - Ixy[i])) * (Y_Yc)[i] for i in range(total)]

for i in range(total):
    print Iyy[i], '\t\t', Sigma[i] / 10 ** 6

print '\nLeast value of Ixx:', min(Ixx)
