from pylab import *

path = 'C:\\Users\\Waffles Crazy Peanut\\Desktop\\Dropbox\\ADP\\Week 5 (Reset)\\'
data = ['Aspect Ratio', 'Cruise Altitude', 'Cruise Velocity', 'Empty Weight', 'Fineness Ratio', 'Fuselage Width', 'Height', 'Landing Speed', 'Length of Aircraft', 'Maximum Fuel Capacity', 'Maximum Landing Weight', 'Maximum Speed', 'Maximum Takeoff Weight', 'Payload', 'Range', 'Runway Length', 'Service Ceiling', 'Taper Ratio', 'Thrust Loading', 'Wing Area', 'Wing Loading', 'Wing Span']
units = ['no\ unit', 'm', 'no\ unit', 'N', 'no\ unit', 'm', 'm', 'knots', 'm', 'l', 'N', 'no\ unit', 'N', 'N', 'km', 'm', 'm', 'no\ unit', 'no\ unit', 'm^2', 'Nm^{-2}', 'm']

def get():          # For getting the input
    f = []
    n = int(raw_input('Number of aircrafts: '))
    for i in range(n):
        i = 0
        a = raw_input('\nAircraft name: ')
        s = [a]
        while i < len(data):
            k = raw_input(data[i] + ': ')
            s.append(k)
            i += 1
        f.append(s)
    return f

def write(s):       # For appending the given input
    f = open(path + 'Data.txt', 'a')
    i = 0
    j = 0
    while j < len(max(s)):
        while i < len(s):
            f.write(s[i][j] + '\t')
            i += 1
        if i == len(s) and j < len(max(s)):
            i = 0
        f.write('\n')
        j += 1
    f.close()

def dplot(s = None):      # If you have already have the input, copy-paste from Excel to notepad with a 'tab' at the end of each line
    dx = 0.2
    dy = 0.3
    ddx = 0
    ddy = 0.02
    c = 12000
    dr = 0.2
    d = []
    a = []
    p = []
    with open(path + 'Data.txt', 'r') as file:
        f = file.readlines()
    names = f[0].split('\t')[:-1]
    r = [float(i) for i in f[15].split('\t')[:-1]]
    if not s:
        for i in range(len(data)):
            print '\t' + str(i + 1) + ':', data[i]
        s = int(raw_input('\nEnter your choice: '))
    if s <= len(data):
        m = f[s].split('\t')[:-1]
        for i in range(len(r)):
            if m[i] != '':
                a.append(r[i])
                d.append(float(m[i]))
                p.append(i + 1)
        r = a
        z = rmin(s)
        r.append(z[0])
        d.append(z[1])
        plot(r, d, 'ro')          # Plots the list with indices at some tolerance
        axis([min(r) * (1 - dx), max(r) * (1 + dx), min(d) * (1 - dy), max(d) * (1 + dy)])
        xlabel(r'Range $\mathregular{[km]}$', fontsize = 18)
        ylabel(data[s - 1] + r' $\mathregular{[' + units[s - 1] + r']}$', fontsize = 18)
##            circle = Circle((c, (max(d) + min(d)) / 2.0), max(d) * dr, color = 'b', fill = False)
##            fig=gcf()
##            fig.gca().add_artist(circle)
        r = r[:-1]
        d = d[:-1]
        for i in range(len(r)):
            (x, y) = (r[i] + r[i] * ddx, d[i] + d[i] * ddy)
            text(x, y, r'$\mathbf{' + str(p[i]) + r'}$', fontsize = 16, bbox = dict(facecolor = 'blue', alpha = 0.15))
        grid(True)
        savefig(str(s) + ' - ' + data[s - 1])
        show()
    else:
        return None
    return None

def rmin(s, ran = 14000):        # To find the minimum point for a given range (using Euclidean distance)!
    with open(path + 'Data.txt', 'r') as file:
        f = file.readlines()
    ranges = [float(i) for i in f[15].split('\t')[:-1]]
    data = [float(i) for i in f[s].split('\t')[:-1] if len(i)]
    y = min(data)
    y0 = max(data)
    s = (ranges[0] - ran) ** 2 + (data[0] - y) ** 2
    t = 0
    dy = (y0 - y) / 100.0
    p = 0
    while y < y0:
        k = [sqrt((ran - ranges[i]) ** 2 + (y - data[i]) ** 2) for i in range(len(data))]
        if sum(k) < s:
            s = sum(k)
            t = y
            p = k.index(max(k)) + 1
        y += dy
    return (ran, t, p)
