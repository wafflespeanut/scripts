from pylab import *
execfile("Standard Atmosphere.py")

path='C:\\Users\\Waffles Crazy Peanut\\Desktop\\Dropbox\\ADP\\Week 6 (Reset)\\Iter.txt'

def fan(w0=393085,we=177945,tl=0.27665,ca=10752,cv=0.85,wp=52960,wc=2000,r=14000,n=4):
    a=[]; cv*=((1.4*287*atmos(ca)[0])**0.5)*(18.0/5); wf=0; rf=0.4; wpp=0; d0=1.225; i=0; re=re0=float(we)/w0
    while True:                             # For Turbojet/Turbofan engines
        try:
            a.append([w0,we,wpp,wf,re,rf])
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
        except KeyboardInterrupt:       # Ctrl-C resets the values for current iteration
            if i==0:
                print '\n\tThis is the first iteration!'
                w0,we,wpp,wf,re,rf = (z for z in a[i]); del a[-1]; continue
            try:
                w0,we,wpp,wf,re,rf = (z for z in a[i]); del a[-1]
                raw_input('\n\t(Resetting values!) Press [Enter] to continue...')
            except KeyboardInterrupt:       # Pressing Ctrl-C again takes back to previous iteration
                i-=1; w0,we,wpp,wf,re,rf = (z for z in a[i]); del a[-1]
                print '\n\t(Getting back to previous iteration...)\n'

def prop(w0=14333,we=7400,pl=0.294906,ca=8000,cv=500,wp=3600,wc=400,r=1800,n=2):
    wf=0; rf=0.15; wpp=0; d0=1.225; i=0; re=re0=float(we)/w0
    while True:                             # For Turboshaft/Turboprop engines
        print '\nIteration %s'%(i)
        w0=(wc+wp+wpp+wf)/(1-re-rf)
        print '\nNet weight: %s kg'%(w0)
        p=w0*pl*1.2
        print 'Power (per engine): %s shp'%(p/n)
        wpp=float(raw_input('Engine Weight (lb): '))*0.4535924*n
        pe=float(raw_input('Engine Power (shp): '))*n
        pc=pe*(atmos(ca)[2]/d0)**1.2
        print 'Cruise Power (per engine): %s shp'%(pc/n)
        sfc=float(raw_input('SFC (lb/lbf-hr): '))
        wf=(sfc*pc*r*1.2*0.4535924)/(cv); rf=0; re=re0-wpp/w0
        print 'Fuel Weight ratio: %s'%(wf/w0)
        print 'Empty Weight ratio: %s'%(re)
        raw_input('\nPress [Enter] to continue...'); i+=1

def iterplot():
    i=2; d=[]
    with open(path,'r') as file: data=file.readlines()
    while i<len(data):
        if 'Iteration' in data[i]: i+=2; d.append(float(data[i].split(' ')[2]))
        i+=1
    x=range(1,len(d)+1); plot(x,d,'ro'); plot(x,d); axis([0,len(x)+1,min(d)*0.95,max(d)*1.1])
    xlabel(r'Iteration $\mathregular{[no\ unit]}$',fontsize=18); ylabel(r'Net Weight $\mathregular{[kg-f]}$',fontsize=18)
    grid(True); show()
