def fibo(n):
    a = [0, 1]
    while True:
        a.append(a[-1] + a[-2])
        if len(str(a[-1])) == n:
            break
    return len(a) - 1

# n = 1000
# print "The first term in the Fibonacci series to contain " + str(n) + " digits: " + str(fibo(1000))
