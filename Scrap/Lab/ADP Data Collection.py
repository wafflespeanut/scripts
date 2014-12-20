from pylab import *
from random import choice

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

def dplot():
    with open(path+'Data.txt','r') as file: f=file.readlines()
    n=f[0].split('\t')[:-1]; r=[float(i) for i in f[11].split('\t')[:-1]]
    for i in range(len(data)): print '\t'+str(i+1)+':',data[i]
    s=int(raw_input('\nEnter your choice: '))
    if s<=len(data):
        try:
            d=[float(i) for i in f[int(s)].split('\t')[:-1]]
            plot(r,d,'ro'); axis([0,max(r)*1.2,0,max(d)*1.2])
            for i in range(100): x=choice([1,-1]); y=choice([1,-1])
            grid(True); show()
        except ValueError: print '\nValues are missing!'
    else: return None

##text(1.1,1.1,r'$\mathbf{1}$',fontsize=15,bbox=dict(facecolor='blue',alpha=0.2))
