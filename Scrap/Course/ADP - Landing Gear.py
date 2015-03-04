import math

wdict={1:'main wheel',2:'nose wheel'}

for i in range(1,3):
    w0=404796.621304*2.204622; c=0; z=wdict[i]
    nwl=w0*0.1; mwl=w0*0.9
    do=float(raw_input('Outer diameter of %s (in): '%(wdict[i])))
    db=float(raw_input('Width of %s (in): '%(wdict[i])))
    di=float(raw_input('Inner diameter of %s (in): '%(wdict[i])))
    rr=float(raw_input('Rolling radius of %s (in): '%(wdict[i])))
    ap=2.3*(db*do)**0.5*(do/2-rr); print 'Projected area of %s: %s in^2'%(wdict[i],ap)
    pt=float(raw_input('Tyre pressure of %s (psi): '%(wdict[i]))); wts=pt*ap
    print 'Tyre supporting weight of %s: %s lb'%(wdict[i],wts)
    n=math.ceil(mwl/wts); print 'Least number of tyres required for %s: %s '%(wdict[i],n)
    mdb=float(raw_input('Maximum width of %s (in): '%(wdict[i])))
    a=((do/2)**2-rr**2)**0.5; print 'Semi-major axis of projected ellipse in %s: %s in'%(wdict[i],a)
    ac=math.pi*(mdb/2)*a; print 'Area of contact of %s: %s in^2'%(wdict[i],ac)
    area=ac*n; print 'Total contact area of %s: %s in^2'%(wdict[i],area); c+=area
rl=w0/c; print 'Runway loading: %s psi'%(rl*0.6894757293178307)
