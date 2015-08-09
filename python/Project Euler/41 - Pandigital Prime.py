execfile("7 - 10001st Prime.py")
from itertools import permutations

plist = sieve(int(999999999 ** 0.5) + 1)

def check(n):
    r = int(n ** 0.5 + 1)
    if n % 2 == 0:
        return False
    for i in plist:
        if not n % i and i != n:
            return False
    return True

def genpan(r):
    l = '1234567890'[:r]
    t = list(permutations(l))
    a = []
    for i in t:
        a.append(int(''.join(i)))
    return a

def panprimes():
    t = 0
    for n in range(1, 10):
        for i in genpan(n):
            if check(i) and i > t:
                t = i
    return t

# print str(panprimes()) + " is the largest pandigital prime number that exists!"
