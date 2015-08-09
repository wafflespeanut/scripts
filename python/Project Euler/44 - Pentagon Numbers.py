def pen(r):
    a = set()
    for n in range(1, r + 1):
        a.update([n * (3 * n - 1) / 2])
    return a

def sumdif(r):
    a, b = pen(r / 2), pen(r)
    c, p = [], set()
    for i in a:
        for j in a:
            if i + j in b:
                c.append([i, j])
    for i in c:
        if abs(i[0] - i[1]) in a:
            p.update(i)
    return p

# r = 5000
# s = list(sumdif(r))
# print "The pentagonal pair whose difference is minimum: " + str(s) + " with difference " + str(abs(s[1] - s[0]))
