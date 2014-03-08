bal=999999
air=0.2
mir=air/12
low=bal/12
high=(bal*(1+mir)**12)/12
obal=bal
tiny=0.01
while abs(obal)>tiny:
    obal=bal
    mp=(high-low)/2+low
    for month in range(12):
        obal-=mp
        obal*=1+mir
    if obal>0:
        low=mp
    else:
        high=mp

print "Lowest mp:", round(mp, 2)
