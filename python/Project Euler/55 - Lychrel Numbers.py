def lychrel(n, r):
    i = 1
    m = n + int(str(n)[::-1])
    while i <= r:
        if str(m) == str(m)[::-1]:
            return False
        m += int(str(m)[::-1])
        i += 1
    return True

def find(r, i):
    s = 0
    for n in range(1, r):
        if lychrel(n, i):
            s += 1
    return s

# i, r = 50, 10000
# print "There are " + str(find(r, 50)) + " Lychrel numbers below " + str(r) + "!"
