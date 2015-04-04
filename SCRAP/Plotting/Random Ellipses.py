from pylab import *
from matplotlib.patches import Ellipse

n=250; ells=[Ellipse(xy=rand(2)*10,width=rand(),height=rand(),angle=rand()*360) for i in range(n)]

fig = figure(); ax = fig.add_subplot(111, aspect='equal')
for e in ells:
    ax.add_artist(e); e.set_clip_box(ax.bbox)
    e.set_alpha(rand()); e.set_facecolor(rand(3))

xlim(0,10); ylim(0,10); show()
