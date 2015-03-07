from pylab import *

def get(s):
    a=[]; print "Enter {}...".format(s)
    while True:
        try:
            g=raw_input()
            if g=="": break
            a.append(float(g))
        except ValueError: return None
    return a

def output():       # For plotting two things with respect to something
    X=get('X'); Y1=get('Y1'); Y2=get('Y2')
    l1=str(raw_input('Label 1:')); l2=str(raw_input('Label 2:'))
    figure(figsize=(10,6),dpi=80)
    plot(X,Y1,color="blue",linewidth=2.5,linestyle="-",label=l1)
    plot(X,Y2,color="red",linewidth=2.5,linestyle="--",label=l2)
    legend(loc='lower right')
    show()
