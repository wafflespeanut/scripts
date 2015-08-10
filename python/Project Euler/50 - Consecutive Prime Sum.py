execfile("7 - 10001st Prime.py")

def psum(a, r):
    plist = sieve(10 ** len(str(r)) - 1)
    s, t, m = 0, 0, 1
    if a not in plist:
        return False
    else:
        k = plist[plist.index(a): ]
    for i in k:
        t += i
        if t < r and t in plist:
            s = t
            m = plist.index(i) - plist.index(a) + 1
    return [s, m]

# k, r = 7, 999999      # After some trial & errors...
# print "Starting from " + str(k) + ', the prime ' + str(psum(k, r)[0]) + " can be written as a sum of " + str(psum(k, r)[1]) + " consecutive primes!"
