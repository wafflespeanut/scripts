def sumSq(n):
    temp = 0
    for i in range(n + 1):
        temp += i ** 2
    return temp

def sqSum(n):
    temp = 0
    for i in range(n + 1):
        temp += i
    return temp ** 2

# print "The difference between sum of squares and square of sums of first 100 natural numbers: " + str(sqSum(100) - sumSq(100))
