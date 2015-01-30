execfile("Standard Atmosphere.py")

def find(w0=275300,we=130199,tl=0.2659,ca=10448,cv=0.83505,wp=51720,wc=2240,r=7000,n=4):
    cv*=((1.4*287*atmos(ca)[0])**0.5)*(18.0/5); wf=0; rf=0.3; wpp=0; d0=1.225; i=0; re=re0=float(we)/w0
    while True:
        print '\nIteration %s'%(i)
        w0=(wc+wp+wpp+wf)/(1-re-rf)
        print '\nNet weight: %s kg'%(w0)
        t=w0*tl*9.81*1.2
        print 'Thrust (per engine): %s lbf'%(t/(4.448*n))
        wpp=float(raw_input('Engine Weight (lb): '))*0.4535924*n
        te=float(raw_input('Engine Thrust (lbf): '))*4.448*n
        tc=te*(atmos(ca)[2]/d0)**1.2
        print 'Thrust at Cruise (per engine): %s N'%(tc/n)
        sfc=float(raw_input('SFC (lb/lbf-hr): '))
        wf=(sfc*tc*r*1.2)/(cv*9.81); rf=0; re=re0-wpp/w0
        print 'Fuel Weight ratio: %s'%(wf/w0)
        print 'Empty Weight ratio: %s'%(re)
        raw_input('\nPress [Enter] to continue...'); i+=1
