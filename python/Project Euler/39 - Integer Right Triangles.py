def sols(k):
    a, p = 0, {}
    for n in range(k + 1):
        for b in range(1, n / 2):
            a = (n * n / 2 - n * b) / (n - b)
            c = n - a - b
            if a ** 2 + b ** 2 == c ** 2:
                if a + b + c in p:
                    p[a + b + c] += 1
                else:
                    p[a + b + c] = 1
    return p

def findsol(r):
    plist = sols(r)
    t = [0, 0]
    for i in plist:
        if plist[i] > t[1]:
            t[0], t[1] = i, plist[i]
    return t

# n = 1000
# p=findsol(n)
# print "The perimeter (within " + str(n) + ") having the maximum number of solutions is: " + str(p[0]) + " with " + str(p[1]) + " solutions!"
