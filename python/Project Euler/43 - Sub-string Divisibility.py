execfile("41 - Pandigital Prime.py")

def find(r):
    a = []
    plist = genpan(r)
    s = sieve(18)
    for i in plist:
        k, c = 0, 0
        while k < 7:
            m = int(str(i)[k + 1: k + 4])
            if not m % s[k]:
                c += 1
            else:
                break
            k += 1
        if c == len(s):
            a.append(i)
    return a

# n = 10
# s = sum(find(n))
# print "The sum of all 0-9 pandigital numbers with the property is: " + str(s)
