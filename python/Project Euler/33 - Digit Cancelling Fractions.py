def cancel(i1, i2):      # Built only for two digits
    s, s1, s2 = [], str(i1), str(i2)
    for i in s1:
        if i not in s2:
            s.append(int(i))
    for i in s2:
        if i not in s1:
            s.append(int(i))
    if len(s) == 2 and 0 not in s:
        if float(i1) / i2 == float(s[0]) / s[1]:
            return True
    else:
        return False

def curious(r):
    nontrivial = []
    for i in range(10, r + 1):
        for j in range(10, r + 1):
            if i != j and float(i) / j < 1 and i % 10 != 0:
                if cancel(i, j):
                    nontrivial.append([i, j])
    return nontrivial

def product(a):
    p1, p2 = 1, 1
    for i in a:
        p1 *= i[0]
        p2 *= i[1]
    return [p1, p2]

# fracs = product(curious(100))
# print "The product of fractions returns " + str(fracs[0]) + " in the numerator, and " + str(fracs[1]) + " in the denominator!"
