# If you wanna access cpropep using Python, add a string value "Autorun"="CD /d C:\\cpropep"
# to [HKEY_CURRENT_USER\Software\Microsoft\Command Processor]

from pylab import *
from os import system

p1='C:\cpropep\input.pro'
p2='C:\cpropep\output.pro'

#   AP  - 108       Al  - 34        CTPB - 265      482  -  HTPB
#   AN  - 114       FeO - 375       DA   - 327      491  -  IPDI
#   Mg  - 558       LiF - 545       TDA  - 905      

prop=[265,327,905,34,108,375]   # Compound index as per listed in 'cpropep'
w=[20,3.75,1.25,10,63,2]        # Weight in grams

def inwrite(prop,w):        # Writes the input for 'cpropep' command-line
    F='Propellant\n'; i=0
    while i<len(prop): F+='+'+str(prop[i])+'   '+str(w[i])+' g\n'; i+=1
    for i in range(20,201,20):
        F+='\nHP\n'; F+='+chamber_pressure %d bar\n'%(i)
    t=open(p1,'w'); t.write(F); t.close()

def cprop(): p='C:\cpropep\cpropep -f '+p1+' -o '+p2; system(p)

def f(s):
    t=''; i=-1
    while s[i]!=' ': t+=s[i]; i-=1
    return float(t[::-1])

def readval():              # Reads the output from 'cpropep' & computes ISP
    P=[float(i) for i in range(20,201,20)]; T=[]; M=[]; G=[]; V=[]; SP=[]; k=0
    F=open(p2,'r'); List=''
    for i in F: List+=i
    l=List.split('\n')
    for i in l:
        if 'Temperature (K)' in i: T.append(f(i))
        elif 'M (g/mol)' in i: M.append(f(i))
        elif 'Gamma' in i: G.append(f(i))
    while k<len(P):
        g=(G[k]-1)/G[k]
        m=(((2*8314*T[k])/(g*M[k]))*(1-(1/P[k])**g))**0.5
        V.append(m); SP.append(m/9.81); k+=1
    F.close(); return SP

def values():               # Appends values into a file for using in Excel
    path='C:\cpropep\PYTHON.txt'
    inwrite(prop,w); cprop(); f=open(path,'a')
    a=[str(i)+'\n' for i in readval()]
    f.write(''.join(a)+'\n'); f.close()

def plotall():              # Plots ISP vs Chamber pressure
    inwrite(prop,w); cprop(); SP=array(readval())
    P=arange(20,201,20); figure(figsize=(10,6),dpi=80)
    xlim(P.min(),P.max()); ylim(SP.min()-10,SP.max()*1.05)
    plot(P,SP,color="blue",linewidth=2.5,linestyle="-",label="ISP")
    legend(loc='upper left'); show()
