# Triangle used in problem

##    75
##    95 64
##    17 47 82
##    18 35 87 10
##    20 04 82 47 65
##    19 01 23 75 03 34
##    88 02 77 73 07 63 67
##    99 65 04 28 06 16 70 92
##    41 41 26 56 83 40 80 70 33
##    41 48 72 33 47 32 37 16 94 29
##    53 71 44 65 25 43 91 52 97 51 14
##    70 11 33 28 77 73 17 78 39 68 17 57
##    91 71 52 38 17 14 91 43 58 50 27 29 48
##    63 66 04 68 89 53 67 30 73 16 69 87 40 31
##    04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

def getTri():
    t=raw_input("Enter raw data...\n")
    t=t.split('\n'); new=[]
    for i in t: new.append(i.split(' '))
    return new

def compare(big,small):
    eff=[]; t=[]
    for i in range(len(small)):
        t.extend([small[i]+big[i],small[i]+big[i+1]])
        eff.append(max(t[-2:]))
    return eff

def formInt(get):
    new=[]
    for i in get:
        t=[]
        for j in i:
            t.append(int(j))
        new.append(t)
    return new

def find():
    get=getTri()
    Tri=formInt(get); i=len(Tri)-1
    while i>0:
        temp=compare(Tri[i],Tri[i-1])
        Tri[i-1]=temp; i-=1; Tri=Tri[:-1]
    return Tri

#print "The maximum total from top to bottom of the triangle is " +str(find()[0][0])
