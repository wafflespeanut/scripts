from pylab import *
from random import choice

eqs = []
eqs.append((r"$\int_{-\infty}^\infty e^{-x^2}dx=\sqrt{\pi}$"))
eqs.append((r"$\nabla \cdot \mathbf{E}=\frac{\rho}{\epsilon_0}$"))
eqs.append((r"$E=h\nu$"))
eqs.append((r"$\Delta x.\Delta p\geq\frac{\hbar}{2}$"))
eqs.append((r"$\nabla \times \mathbf{E}=-\frac{\partial B}{\partial t}$"))
eqs.append((r"$\langle E\rangle=\frac{3}{2} kT$"))
eqs.append((r"$\nabla \cdot \mathbf{B}=0$"))
eqs.append((r"$E=\gamma mc^2$"))
eqs.append((r"$\nabla \times \mathbf{B}=\frac{1}{c^2}( \frac{\partial E}{\partial t}+\frac{\mathbf{J}}{\epsilon_0})$"))
eqs.append((r"$E=\sqrt{{m_0}^2c^4 + p^2c^2}$"))
eqs.append((r"$F_G=G\frac{m_1m_2}{r^2}$"))

axes([0.025, 0.025, 0.95, 0.95])
n = 50

for i in range(n):
    eq = choice(eqs)
    size = np.random.uniform(10, 35)
    x, y = np.random.uniform(0, 1, 2)
    alpha = np.random.uniform(.1, .8)
    text(x, y, eq, ha = 'center', va = 'center', color = "#000000", alpha = alpha, 
         transform = gca().transAxes, fontsize = size, clip_on = True)

xticks([]), yticks([])
show()
