execfile("Standard Atmosphere.py")

def find(w0=275300,we=130199,tl=0.2659,ca=10448,cv=0.83505,wp=45000,wc=1500,r=14000,n=4):
    cv*=((1.4*287*atmos(ca)[0])**0.5)*(18.0/5); wf=0; wpp=0; rf=0.3; d0=1.225
    re=float(we-wpp)/w0; w0=(wc+wp+wpp+wf)/(1-re-rf)
    print '\nNet weight: %s kg'%(w0)
    t=w0*tl*9.81*1.2
    print 'Thrust (per engine): %s lbf'%(t/(4.448*n))
    wpp=float(raw_input('Engine weight (kg): '))*n
    tc=t*(atmos(ca)[2]/d0)**1.2
    print 'Thrust at Cruise (per engine): %s N'%(tc/n)
    sfc=float(raw_input('SFC (lb/lbf-hr): '))
    wf=(sfc*tc*r*1.2)/(cv*9.81); rf=0; we=w0-wc-wp-wf
    print '\nFuel Weight: %s kg'%(wf)
    print 'Empty Weight: %s kg'%(we)
