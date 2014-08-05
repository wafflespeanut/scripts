x=25; epsilon=0.01; guessed=0
low=0.0; high=x;
ans=(high + low)/2.0

while abs(ans**2-x)>=epsilon:
    print("Lower bound: "+ str(low) + "\tHigher bound: "+ str(high) + "\tAnswer = " + str(ans))
    guessed+=1
    if ans**2<x:
        low=round(ans,4)
    else:
        high=round(ans,4)
    ans=(high + low)/2.0

print "\nGuessed " + str(guessed) + " times"
print str(round(ans,4)) + " is close to the square root of " + str(x)
