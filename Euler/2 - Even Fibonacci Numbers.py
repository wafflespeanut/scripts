s=0; i=-1; j=1; c=0

while c<4000000:
    c=i+j
    i=j; j=c
    if c%2==0: s+=c

print "The sum of all even Fibonacci numbers upto 4 milion: " + str(s)
