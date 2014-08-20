def sumSquare(n):
    temp=0
    for i in range(n+1):
        temp+=i**2
    return temp

def squareSum(n):
    temp=0
    for i in range(n+1):
        temp+=i
    return temp**2

print "The difference between sum of squares and square of sums of first 100 natural numbers: " +str(squareSum(100)-sumSquare(100))
