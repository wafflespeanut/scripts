def pfactors(n):    # Mutating factorization
    p = []
    while n % 2 == 0:
        p.append(2)
        n /= 2
    i = 3
    limit = (n + 1) ** 0.5
    while i <= limit:
        if n % i == 0:
            p.append(i)
            n /= i
            limit = (n + i) ** 0.5
        else:
            i += 2
    if n != 1:
        p.append(n)
    return set(p)

def consec(n):
    i, r = 1, 1
    while i <= n:
        if len(pfactors(r)) >= n:
            i += 1
        else:
            i = 1
        r += 1
    return r - n

# n = 4
# print "The first of the " + str(n) + " consecutive integers to have " + str(n) + " distinct prime factors is: " + str(consec(n))
