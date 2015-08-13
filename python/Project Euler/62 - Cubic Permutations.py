execfile("52 - Permuted Multiples.py")

def cube(n):
    return n ** (1 / 3.0)

def cubegen(r1, r2):
    a = []
    n1, n2 = int(round(cube(r1))), int(round(cube(r2)))
    for i in range(n1, n2 + 1):
        a.append(i ** 3)
    return a

def checkperm(n, arr):
    a = []
    for i in arr:
        if isPerm(n, i):
            a.append(i)
    return a

def find(n, st):
    r = int('9' * len(str(st)))
    s = cubegen(st, r)
    for i in s:
        m = checkperm(i, s)
        if m and len(m) == n:
            return m
    return None

# n, start = 5, 111111111111
# s = find(n, start)
# print min(s), 'is the smallest cube having', n, 'cubic permutations!'
