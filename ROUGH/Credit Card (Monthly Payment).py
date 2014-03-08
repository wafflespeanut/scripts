obal=4842
air=0.2
mpr=0.04
irest=0
a=12
count=0
b=obal+irest
for i in range(a):
    print "Month " +str(i+1) +":"
    mp=b*mpr
    print "Minimum monthly payment: " +str(round(mp,2))
    count+=mp
    obal=b-mp
    irest=(air/12)*obal
    b=obal+irest
    print "Remaining obal: " +str(round(b,2))
    
print "Total paid: " +str(round(count,2))
print "Remaining obal: " +str(round(b,2))
