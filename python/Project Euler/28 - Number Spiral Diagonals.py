def spiral(n):
    i, c, diag = 1, 1, 1
    while i < n ** 2:
        r = 1
        while r <= 4:     # each level has 4 rounds
            if c % 2 == 1:
                i += c + 1
                diag += i      # odd number spacing in diagonal numbers
            r += 1
        c += 1
    return diag

# n, s = 1001, spiral(n)
# print "The sum of diagonal numbers in a " + str(n) + " by " + str(n) + " spiral is: " + str(s)
