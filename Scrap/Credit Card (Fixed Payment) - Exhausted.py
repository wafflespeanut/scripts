obal=3329
air=0.2
irest=0
mir=air/12
mp=10
bal=0
while round(bal,-1)>=0:
    bal=obal
    b=obal
    print "Trying " +str(mp)
    for i in range(12):
        bal=round(b-mp,-1)
        irest=mir*bal
        b=bal+irest

    mp+=10

print "Lowest monthly payment: " +str(mp-10)
