from pylab import *

k={'C':12,'O':16,'H':1,'N':14}
h={'c':-396808,'w':-251594,'co':-118902}
cp={'c':60.433,'w':51.143,'co':36.271,'o':37.788,'h':34.236,'n':35.988}
r=8.314; t0=298.15

s='CH4'; hf=-74293      # Input here!

def count(s):
    k={'C':0,'O':0,'H':0,'N':0}; n='1234567890'
    for i,j in enumerate(s):
        if j in k:
            if i==len(s)-1: k[j]+=1; break
            if s[i+1] in n:
                m=''; c=1
                while i+c<len(s) and s[i+c] in n: m+=s[i+c]; c+=1
                k[j]+=int(m)
            else: k[j]+=1
    return k

def sto(s):
    k1=count(s); x=k1['C']; y=k1['H']/2.0; a=(2*x+y)/2
    return (k['C']*k1['C']+k['H']*k1['H'])/(float(a)*(k['O']+3.76*k['N'])*2)

def lean(s,phi):
    p=sto(s); k1=count(s); b=k1['C']; c=k1['H']/2.0
    a=round((k['C']*k1['C']+k['H']*k1['H'])/(phi*(k['O']+3.76*k['N'])*2*p),4)
    d=round((2*a-2*b-c)/2,4)
    return (a,b,c,d)

def rich(s,phi):        # b & e are assumed to be half of number of carbon atoms
    p=sto(s); k1=count(s); b=e=k1['C']/2.0
    a=round((k['C']*k1['C']+k['H']*k1['H'])/(phi*(k['O']+3.76*k['N'])*2*p),4)
    c=round(2*a-e-2*b,4)
    d=round((k1['H']-2*c)/2,4)
    return (a,b,c,d,e)

def cpres(s,hf):        # Adiabatic temperatures for constant pressure process
    k1=count(s); c1,c2,c3,c4,c5=(cp['c'],cp['w'],cp['o'],cp['n'],cp['co']); h1,h2,h3=(h['c'],h['w'],h['co']); arr=[]
    for i in range(1,6):
        phi=0.2*i
        a,b,c,d=lean(s,phi)
        m=round((hf-b*h1-c*h2+t0*(b*c1+c*c2+d*c3+3.76*a*c4))/(b*c1+c*c2+d*c3+3.76*a*c4),4)
        arr.append(m)
    for i in range(1,6):
        phi=1+0.2*i
        a,b,c,d,e=rich(s,phi)
        m=round((hf-b*h1-c*h2-e*h3+t0*(b*c1+c*c2+d*c3+3.76*a*c4+e*c5))/(b*c1+c*c2+d*c3+3.76*a*c4+e*c5),4)
        arr.append(m)
    return arr

def cvol(s,hf):         # Adiabatic temperatures for constant volume process
    k1=count(s); h1,h2,h3=(h['c'],h['w'],h['co']); c1,c2,c3,c4,c5=(cp['c'],cp['w'],cp['o'],cp['n'],cp['co']); arr=[]
    for i in range(1,6):
        phi=0.2*i
        a,b,c,d=lean(s,phi)
        n=a+1
        m=round((hf-b*h1-c*h2+t0*(b*c1+c*c2+d*c3+3.76*a*c4-n*r))/(b*c1+c*c2+d*c3+3.76*a*c4-n*r),4)
        arr.append(m)
    for i in range(1,6):
        phi=1+0.2*i
        a,b,c,d,e=rich(s,phi)
        n=a+1
        m=round((hf-b*h1-c*h2-e*h3+t0*(b*c1+c*c2+d*c3+3.76*a*c4+e*c5-n*r))/(b*c1+c*c2+d*c3+3.76*a*c4+e*c5-n*r),4)
        arr.append(m)
    return arr

def output():           # Plots stuff for given molecule & enthalpy
    phi=[i*0.2 for i in range(1,6)]
    for i in range(1,6): phi.append((1+0.2*i))
    P1=cpres(s,hf); P2=cvol(s,hf)
    figure(figsize=(10,6),dpi=80)
    plot(phi,P1,color="blue",linewidth=2.5,linestyle="-",label="Constant Pressure")
    plot(phi,P2,color="red",linewidth=2.5,linestyle="--",label="Constant Volume")
    legend(loc='upper left')
    show()
