def evenFibo(n):
    s, i, j, c = 0, -1, 1, 0
    while c < n:
        c = i + j
        i, j = j, c
        if c % 2 == 0:
            s += c
    return s

# n = 4000000
# print "The sum of all even Fibonacci numbers upto " + str(n) + " is: " + str(fibonacci(n))
