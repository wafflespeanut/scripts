import math

def landing(w0=404796.621304):
    wdict={1:'main wheel',2:'nose wheel'}; w0*=2.204622; c=0
    for i in range(1,3):
        z=wdict[i]; nwl=w0*0.1; mwl=w0*0.9
        do=float(raw_input('\nOuter diameter of %s (in): '%(z)))
        db=float(raw_input('Width of %s (in): '%(wdict[i])))
        di=float(raw_input('Inner diameter of %s (in): '%(z)))
        rr=float(raw_input('Rolling radius of %s (in): '%(z)))
        ap=2.3*(db*do)**0.5*(do/2-rr); print 'Projected area of %s: %s in^2'%(z,ap)
        pt=float(raw_input('Tyre pressure of %s (psi): '%(z))); wts=pt*ap
        print 'Tyre supporting weight of %s: %s lb'%(z,wts)
        if i==1: wl=mwl
        else: wl=nwl
        n=math.ceil(wl/wts); print 'Least number of tyres required for %s: %s '%(z,int(n))
        n=float(raw_input('Number of tyres (%s): '%z))
        mdb=float(raw_input('Maximum width of %s (in): '%(z)))
        a=((do/2)**2-rr**2)**0.5; print 'Semi-major axis of projected ellipse in %s: %s in'%(wdict[i],a)
        ac=math.pi*(mdb/2)*a; print 'Area of contact of %s: %s in^2'%(z,ac)
        area=ac*n; print 'Total contact area of %s: %s in^2'%(z,area); c+=area
    rl=w0/c; print 'Runway loading: %s psi'%(rl*0.6894757293178307)
