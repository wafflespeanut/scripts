import math

def atmos(alt):
    g=9.80665; R=287
    a01=-0.0065; a23=0.001; a34=0.0028

    def temp(t,a,hmin,hmax): return t+a*(hmax-hmin)

    t0=288.15
    t1=temp(t0,a01,0,11000)
    t2=t1
    t3=temp(t2,a23,20000,32000)
    t4=temp(t3,a34,32000,47000)

    def pres(p,t,t0,a): return p*((t/t0)**(-g/(a*R)))

    def const(f,t,hmin,hmax): return f*(math.e**(-g/(R*t)*(hmax-hmin)))

    p0=101325
    p1=pres(p0,t1,t0,a01)
    p2=const(p1,t2,11000,20000)
    p3=pres(p2,t3,t2,a23)

    def dens(d,t,t0,a): return d*((t/t0)**(-g/(a*R)-1))

    d0=p0/(R*t0)
    d1=dens(d0,t1,t0,a01)
    d2=const(d1,t2,11000,20000)
    d3=dens(d2,t3,t2,a23)

    if alt==0: te=t0; pr=p0; de=d0
        
    elif alt>0 and alt<=11000:
        te=temp(t0,a01,0,alt)
        pr=pres(p0,te,t0,a01)
        de=dens(d0,te,t0,a01)

    elif alt>11000 and alt<=20000:
        te=t1
        pr=const(p1,te,11000,alt)
        de=const(d1,te,11000,alt)

    elif alt>20000 and alt<=32000:
        te=temp(t2,a23,20000,alt)
        pr=pres(p2,te,t2,a23)
        de=dens(d2,te,t2,a23)

    elif alt>32000 and alt<=47000:
        te=temp(t3,a34,32000,alt)
        pr=pres(p3,te,t3,a34)
        de=dens(d3,te,t3,a34)

    else:
        print "INVALID INPUT: Altitude undefined over the given limits!"

    print "Temperature: " +str(round(te,2)) +" K"
    print "Pressure: " +str(round(pr,4)) +" Pa"
    print "Density: " +str(round(de,4)) +" kg/cu.m"
    return None

#alt=float(raw_input("Altitude (meters): ")); atmos(alt)
