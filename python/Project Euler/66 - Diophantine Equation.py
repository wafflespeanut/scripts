def chakra(d):          # Chakravala method
    m, k, x0, y = 1, 1, 1, 0
    if int(d ** 0.5) == d ** 0.5:
        return None
    while k != 1 or y == 0:
        m = k * (m / k +1) - m
        m = m - int((m - d ** 0.5) / k) * k 
        x = (m * x0 + d * y) / k
        y = (m * y + x0) / k
        k = (m ** 2 - d) / k
        x0 = x
    return (abs(x), abs(y))

def expand(d):          # Continued fraction expansion
    t, m = 0, 1
    a = int(d ** 0.5)
    if a == d ** 0.5:
        return None
    n0, d0, n1, d1 = a, 1, 1, 0
    while (n0 ** 2 - d * d0 ** 2) != 1:
        t = m * a - t
        m = (d - t ** 2) / m
        a = int((d ** 0.5 + t) / m)
        n2 = n1
        n1 = n0
        d2 = d1
        d1 = d0
        n0 = a * n1 + n2
        d0 = a * d1 + d2
    return (n0, d0)

def find(r, method):
    t = [0, 0]
    for i in range(2, r + 1):
        m = method(i)
        if m:
            if m[0] > t[1]:
                t = [i, m[0], m[1]]
    return t

# r = 1000
# s = find(r, expand)
# print "When D = " + str(s[0]) + ", the largest value of x in minimal solutions of (x,y) are obtained!", (s[1], s[2])
