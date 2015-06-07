def calc():             # For solving heat-transfer problems using the tri-diagonal matrix method
    n = int(raw_input('Size of Matrix: '))
    a = [0] * n
    b = [0] * n
    c = [0] * n
    p = [0] * (n + 1)
    q = [0] * (n + 1)
    d = [0] * n
    t = [0] * (n + 1)
    for i in range(n):
        if i > 0:
            c[i] = float(raw_input('c' + str(i + 1) + ': '))
        a[i] = float(raw_input('a' + str(i + 1) + ': '))
        if i < (n - 1):
            b[i] = float(raw_input('b' + str(i + 1) + ': '))
        d[i] = float(raw_input('d' + str(i + 1) + ': '))
    c[0] = 0
    b[n - 1] = 0
    print '\nElement variables...\n'
    for i in range(n):
        p[i + 1] =- b[i] / (a[i] + c[i] * p[i])
        q[i + 1] = (d[i] - c[i] * q[i]) / (a[i] + c[i] * p[i])
        print 'p{}: {}\t\tq{}: {}'.format(i + 1, round(p[i + 1], 5), i + 1, round(q[i + 1], 5))
    print '\nTemperatures...\n'
    for i in range(n)[: : -1]:
        t[i] = p[i + 1] * t[i + 1] + q[i + 1]
        print 'T%s: %s' % (i + 1, round(t[i], 5))
