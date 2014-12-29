from pylab import *

path='C:\\Users\\Waffles Crazy Peanut\\Desktop\\Dropbox\\ADP\\'
data=['Aspect Ratio', 'Cruise Altitude', 'Cruise Velocity', 'Empty Weight', 'Fineness ratio', 'Fuselage Width', 'Height', 'Landing Speed', 'Length of Aircraft', 'Maximum Landing Weight', 'Maximum Rate of Climb', 'Maximum Service Ceiling', 'Maximum Speed', 'Maximum Takeoff Weight', 'Payload', 'Range', 'Runway Length', 'Seating Capacity', 'Service Ceiling', 'Thrust Loading', 'Thrust per Engine', 'Wing Area', 'Wing Loading', 'Wing Span']
units=['no\ unit','m','no\ unit','kg','no\ unit','m','m','knots','m','kg','ms^{-1}','m','no\ unit','kg','kg','km','m','seats','m','no\ unit','N','m^2','kgm^{-2}','m']

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
    dx=0.08; dy=0.2; ddx=0; ddy=0.02; c=12000; dr=0.2; d=[]; a=[]; p=[]
    with open(path+'Data.txt','r') as file: f=file.readlines()
    names=f[0].split('\t')[:-1]; r=[float(i) for i in f[15].split('\t')[:-1]]
    if not s:
        for i in range(len(data)): print '\t'+str(i+1)+':',data[i]
        s=int(raw_input('\nEnter your choice: '))
    if s<=len(data):
        m=f[s].split('\t')[:-1]
        for i in range(len(r)):
            if m[i]!='': a.append(r[i]); d.append(float(m[i])); p.append(i+1)
        r=a; print r,'\n',d; plot(r,d,'ro'); axis([min(r)*(1-dx),max(r)*(1+dx),min(d)*(1-dy),max(d)*(1+dy)])
        xlabel(r'Range $\mathregular{[km]}$',fontsize=18); ylabel(data[s-1]+r' $\mathregular{['+units[s-1]+r']}$',fontsize=18)
##            circle=Circle((c,(max(d)+min(d))/2.0),max(d)*dr,color='b',fill=False)
##            fig=gcf(); fig.gca().add_artist(circle)
        for i in range(len(r)):
            (x,y)=(r[i]+r[i]*ddx,d[i]+d[i]*ddy)
            text(x,y,r'$\mathbf{'+str(p[i])+r'}$',fontsize=16,bbox=dict(facecolor='blue',alpha=0.15))
        grid(True); show()
    else: return None
    return None

def rmin(data,ranges,ran=14000):        # To find the minimum point!
    y=min(data); y0=max(data); s=(ranges[0]-ran)**2+(data[0]-y)**2; t=0; dy=(y0-y)/100.0; p=0
    while y<y0:
        k=[sqrt((ran-ranges[i])**2+(y-data[i])**2) for i in range(len(data))]
        if sum(k)<s: s=sum(k); t=y; p=k.index(max(k))+1
        y+=dy
    print "Draw a circle from ({},{}) to point {}!".format(ran,t,p)
