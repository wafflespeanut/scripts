execfile("12 - Highly Divisible Triangular Number.py")
execfile("61 - Cyclical Figurate Numbers.py")

def whichtri(t):
    return int(((1 + 8 * t) ** 0.5 - 1) / 2)
def whichpen(p):
    return int(((1 + 24 * p) ** 0.5 + 1) / 6)

def find(start):
    i = start
    while True:     # Every hexagonal number is triangonal
        if isPen(hexa(i)):
            return i
        i += 1

# k = find(144)
# s = hexa(k)
# h = 'H(' + str(k) + ')'
# p = 'P(' + str(whichpen(s)) + ')'
# t = 'T(' + str(whichtri(s)) + ')'
# print "The next triangular number which is both pentagonal & hexagonal is: " + str(s) + ' = ' + t + ' = ' + p + ' = ' + h
