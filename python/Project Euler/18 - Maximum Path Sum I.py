def getTri(File):
    t = open(File, 'r', 0)
    List, new = '', []
    for i in t:
        List += i
    List = List.split('\n')
    for i in List:
        new.append(i.split(' '))
    return new

def compare(big, small):
    eff, t = [], []
    for i in range(len(small)):
        t.extend([small[i] + big[i], small[i] + big[i + 1]])
        eff.append(max(t[-2:]))
    return eff

def formInt(get):
    new = []
    for i in get:
        t = []
        for j in i:
            t.append(int(j))
        new.append(t)
    return new

def find(File):
    get, Tri = getTri(File), formInt(get)
    i = len(Tri) - 1
    while i > 0:
        temp = compare(Tri[i], Tri[i-1])
        Tri[i-1] = temp
        i -= 1
        Tri = Tri[:-1]
    return Tri

# f = "TRIANGLE_I.TXT"
# print "The maximum total from top to bottom of the triangle is", str(find(f)[0][0]) + '!'
