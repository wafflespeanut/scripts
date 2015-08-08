execfile("7 - 10001st Prime.py")

def rotate(n):
    i, a, s = 1, [n], str(n)
    def rotate(s):
        return s[-1] + s[:-1]
    if len(s) == 1:
        return n
    while i < len(s):
        a.append(int(rotate(str(a[-1]))))
        i += 1
    return a

def needs(n):
    for i in str(n):
        if not int(i) % 2:
            return False
    return True

def checkall(r):
    a, n, p = set(), len(str(r)), sieve(r)
    plist = sieve(10 ** n + 1)
    for i in p:
        if i < 10:
            a.update([i])
            continue
        elif needs(i):
            c, m = 0, rotate(i)
            if i in a:
                continue
            for j in m:
                if j not in plist:
                    break
                else:
                    c += 1
            if c == len(m):
                a.update(m)
    return a

# r = 999999
# s = len(checkall((r / 2)))
# print "There are " + str(s) + " circular primes below 1 million!"
