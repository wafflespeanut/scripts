points = [(0.285, 0.285), (1.425, 0.57), (1.425, 0.57),
          (2.185, 0.617), (3.23, 0.665), (4.18, 0.617),
          (5.13, 0.57), (6.175, 0.52), (6.65, 0.475),
          (6.65, 0.475), (7.41, 0.38), (8.17, 0.285),
          (9.025, 0.095), (8.075, -0.095), (6.65, -0.2375),
          (6.65, -0.2375), (6.08, -0.285), (4.75, -0.38),
          (3.42, -0.42), (2.28, -0.38), (1.425, -0.285),
          (1.425, -0.285), (0.475, -0.19)]

total = len(points)
stingers = [1, 2, 8, 9, 14, 15, 20, 21]
A = [3.4258e-04 if i not in stingers else 0.000748 for i in range(total)]

Ixx, Iyy, Ixy = 1.706548e-07, 1.706548e-07, 0.707591e-07

Ax = [A[i] * points[i][0] for i in range(total)]
Ay = [A[i] * points[i][1] for i in range(total)]

Xc, Yc = sum(Ax) / sum(A), sum(Ay) / sum(A)

X_Xc = [points[i][0] - Xc for i in range(total)]
Y_Yc = [points[i][1] - Yc for i in range(total)]

Ixx_ = [Ixx + A[i] * Y_Yc[i] ** 2 for i in range(total)]
Iyy_ = [Iyy + A[i] * X_Xc[i] ** 2 for i in range(total)]
Ixy_ = [Ixy + A[i] * X_Xc[i] * Y_Yc[i] for i in range(total)]

Sx, Sy = 744413.5006, 178265.8194
Sigma = [((Ixy_[i] * Sx - Ixx_[i] * Sy) / (Ixx_[i] * Iyy_[i] - Ixy_[i] ** 2)) * (X_Xc)[i] +
        ((Ixy_[i] * Sy - Iyy_[i] * Sx) / (Ixx_[i] * Iyy_[i] - Ixy_[i] ** 2)) * (Y_Yc)[i] for i in range(total)]

for i in range(total):
    print i + 1, '\t\t', Ixx_[i], '\t\t', Sigma[i] / 10 ** 6

print '\nLeast value of Ixx:', min(Ixx_)
