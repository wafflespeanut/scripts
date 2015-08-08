execfile("7 - 10001st Prime.py")

def evaluate(num):
    div = []
    for i in plist:
        if int(num % i) == 0:
            div.append(i)
    return max(div)

# n = 600851475143
# plist = sieve(10000)
# print "The largest prime factor of " + str(n) + " is: " + str(evaluate(n))
