def powers(al, ah, bl, bh):
    a = set()
    for i in range(al, ah + 1):
        for j in range(bl, bh + 1):
            a.update([i ** j])
    return len(a)

# s = powers(2, 100, 2, 100)
# print "There are " + str(s) + " distinct terms in the generated sequence!"
