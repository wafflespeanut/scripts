execfile("52 - Permuted Multiples.py")

def permaxi(r):
    t = [0, 0, 10]
    s = ESieve(1, int(1.3 * (r ** 0.5)))
    s = s[int(0.3 * len(s)):]      # 30% deviation
    for i in s:
        for j in s:
            n = i * j
            p = (i - 1) * (j - 1)
            if n > r:
                break
            if isPerm(n, p) and (float(n) / p) < t[2]:
                t = (n, p, float(n) / p)
    if t[2] == 10:
        return None
    return t

# r = 10000000
# s = permaxi(r)
# print "The minimum occurs at n = {}! (Totient: {}, Ratio: {})".format(*s)
