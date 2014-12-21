from pylab import *
from random import choice
from time import sleep

path='C:\\Users\\Waffles Crazy Peanut\\Desktop\\Dropbox\\ADP\\'
data=['Aspect Ratio','Cruise Velocity','Empty Weight','Fineness Ratio','Height','Landing Speed','Length of Aircraft','Maximum Landing Weight','Maximum Rate of Climb','Maximum Service Ceiling','Maximum Speed','Range','Runway Length','Seating Capacity','Service Ceiling','Thrust Loading','Wing Area','Wing Loading','Wing Span']

def get():
    f=[]; n=int(raw_input('Number of aircrafts: '))
    for i in range(n):
        i=0; a=raw_input('\nAircraft name: '); s=[a]
        while i<len(data): k=raw_input(data[i]+': '); s.append(k); i+=1
        f.append(s)
    return f

def write(s):
    f=open(path+'Data.txt','a'); i=0; j=0
    while j<len(max(s)):
        while i<len(s): f.write(s[i][j]+'\t'); i+=1
        if i==len(s) and j<len(max(s)): i=0
        f.write('\n'); j+=1
    f.close()

def dplot(s=None):
    dx=0.08; dy=0.2; ddx=0; ddy=0.02
    with open(path+'Data.txt','r') as file: f=file.readlines()
    n=f[0].split('\t')[:-1]; r=[float(i) for i in f[12].split('\t')[:-1]]
    if not s:
        for i in range(len(data)): print '\t'+str(i+1)+':',data[i]
        s=int(raw_input('\nEnter your choice: '))
    if s<=len(data):
        try:
            d=[float(i) for i in f[int(s)].split('\t')[:-1]]
            if len(r)!=len(d): print '\nValues are missing!'; return None
            plot(r,d,'ro'); axis([min(r)*(1-dx),max(r)*(1+dx),min(d)*(1-dy),max(d)*(1+dy)])
            for i in range(len(r)):
                (x,y)=(r[i]+r[i]*ddx,d[i]+d[i]*ddy)
                text(x,y,r'$\mathbf{'+str(i+1)+r'}$',fontsize=15,bbox=dict(facecolor='blue',alpha=0.15))
            grid(True); show()
        except ValueError: print '\nValues are missing!'
    else: return None
