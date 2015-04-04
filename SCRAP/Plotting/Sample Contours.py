from pylab import *

def f(x,y): return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)

fig=figure(); fig.subplots_adjust(bottom=0.25,left=0.025,top=0.75,right=0.975)

subplot(1,2,1)
n=256; x=np.linspace(-3,3,n); y=np.linspace(-3,3,n)
X,Y=np.meshgrid(x,y)

contourf(X,Y,f(X,Y),8,alpha=.75,cmap='jet')
C=contour(X,Y,f(X,Y),8,colors='black',linewidth=.5)
xticks([]), yticks([])

subplot(1,2,2)
n=256; x=np.linspace(-3,3,n); y=np.linspace(-3,3,n)
X,Y=np.meshgrid(x,y); imshow(f(X,Y))
xticks([]), yticks([])

show()
