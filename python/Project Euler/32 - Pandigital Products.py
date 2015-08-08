def checkpan(r, n):
    s, j = str(n), 0
    l = ''.join([str(i) for i in range(1, r + 1)])
    a = [0 for i in range(r + 1)]
    for i in range(len(s)):
        if s[i] in l:
            a[int(s[i])] += 1
    for i in l:
        if i not in s:
            return False
    while j < len(a):
        if a[j] > 1:
            return False
        j += 1
    return True

def genum(r, n):
    s, a = 0, set()
    for i in range(r + 1):
        for j in range(r + 1):
            s = str(i * j) + str(i) + str(j)
            if len(s) > n:
                break
            if checkpan(n, s):
                a.update([i * j])
    return list(a)

# n, r = 9, 2000
# s = sum(genum(r, n))     # A stupid guess!
# print "The sum of all products whose multiplicand/multiplier/product identity can be written as 1 through 9 pandigital is: " + str(s)
