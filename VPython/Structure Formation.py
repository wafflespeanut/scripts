from visual import *
from time import clock
from random import random,uniform
import numpy
import math

# Sets up a bunch of masses and lets them move under the influence of their
# mutual gravity.
# Masses are put in random positions within a sphere originally. An additional
# force is applied which simulates an equal density distributed over the
# rest of the universe outside this initial sphere.


def randomdirection():
      # Generates random direction on sky.
      # RA (in radians)
      # Dec (in radians)
      ra = 2.0*math.pi*random()
      dec = math.acos(2.0*random()-1.0)-0.5*math.pi
      return ra,dec

def ranvec():
      # Generates a randomly orientated unit vector.
      theta, phi = randomdirection()
      z = math.sin(phi)
      x = math.cos(phi)*math.sin(theta)
      y = math.cos(phi)*math.cos(theta)
      vec = numpy.array([x,y,z])
      return vec


# Stars interacting gravitationally
# Program uses numpy arrays for high speed computations


Nstars = 400  # change this to have more or fewer stars

G = 6.7e-11 # Universal gravitational constant

# Typical values
Msun = 2E30
Rsun = 3E8
Rtrail = 2e8
L = 4e10
vsun = 0.9*sqrt(G*Msun/Rsun)
h0 = 2.5e-6 # Hubble's constant - expansion rate 2.5e-6 is good.

scene = display(title="Stars", width=1300, height=740,
                range=L, forward=(-1,-1,-1))


Stars = []
poslist = []
plist = []
mlist = []
rlist = []
p0 = 0.0*Msun*100000.0

for i in range(Nstars):
    vec = L*ranvec()*(random()**0.3333)
    x = vec[0]
    y = vec[1]
    z = vec[2]
    r = Rsun
    col0 = (uniform(0.7,1.0),uniform(0.7,1.0),
                  uniform(0.7,1.0))
    Stars = Stars+[sphere(pos=(x,y,z), radius=r, color=col0)]
    mass = Msun
    px = p0*uniform(-1,1)
    py = p0*uniform(-1,1)
    pz = p0*uniform(-1,1)
    poslist.append((x,y,z))
    plist.append((px,py,pz))
    mlist.append(mass)
    rlist.append(r)

pos = array(poslist)
p = array(plist)
m = array(mlist)
m.shape = (Nstars,1) # Numeric Python: (1 by Nstars) vs. (Nstars by 1)
radius = array(rlist)

vcm = sum(p)/sum(m) # velocity of center of mass
p = p-m*vcm # make total initial momentum equal zero

dt = 100.0
Nsteps = 0
pos = pos+(p/m)*(dt/2.) # initial half-step
time = clock()
Nhits = 0

while 1:
    rate(100)

    L *= 1.0+h0*dt
    con = 0.9*G*Nstars*Msun/(L*L*L)# strength of force to allow for external mass
    
    # Compute all forces on all stars
    try:  # numpy
        r = pos-pos[:,newaxis] # all pairs of star-to-star vectors
        for n in range(Nstars):
            r[n,n] = 1e6  # otherwise the self-forces are infinite
        rmag = sqrt(add.reduce(r*r,-1)) # star-to-star scalar distances
        hit = less_equal(rmag,radius+radius[:,newaxis])-identity(Nstars)
        hitlist = sort(nonzero(hit.flat)[0]).tolist() # 1,2 encoded as 1*Nstars+2
        F = G*m*m[:,newaxis]*r/rmag[:,:,newaxis]**3 # all force pairs
    except: # old Numeric
        r = pos-pos[:,NewAxis] # all pairs of star-to-star vectors
        for n in range(Nstars):
            r[n,n] = 1e6  # otherwise the self-forces are infinite
        rmag = sqrt(add.reduce(r*r,-1)) # star-to-star scalar distances
        hit = less_equal(rmag,radius+radius[:,NewAxis])-identity(Nstars)
        hitlist = sort(nonzero(hit.flat)) # 1,2 encoded as 1*Nstars+2
        F = G*m*m[:,NewAxis]*r/rmag[:,:,NewAxis]**3 # all force pairs
        
    for n in range(Nstars):
        F[n,n] = 0  # no self-forces
    p = p+sum(F,1)*dt+pos*con*dt*m

    # Having updated all momenta, now update all positions         
    pos = pos+(p/m)*dt

    # Expand universe
    pos *= 1.0+h0*dt

    # Update positions of display objects; add trail
    for i in range(Nstars):
        Stars[i].pos = pos[i]

    # If any collisions took place, merge those stars
    for ij in hitlist:
        i, j = divmod(ij,Nstars) # decode star pair
        if not Stars[i].visible: continue
        if not Stars[j].visible: continue
        # m[i] is a one-element list, e.g. [6e30]
        # m[i,0] is an ordinary number, e.g. 6e30
        newpos = (pos[i]*m[i,0]+pos[j]*m[j,0])/(m[i,0]+m[j,0])
        newmass = m[i,0]+m[j,0]
        newp = p[i]+p[j]
        newradius = Rsun*((newmass/Msun)**(1./3.))
        iset, jset = i, j
        if radius[j] > radius[i]:
            iset, jset = j, i
        Stars[iset].radius = newradius
        m[iset,0] = newmass
        pos[iset] = newpos
        p[iset] = newp
        Stars[jset].visible = 0
        p[jset] = vector(0,0,0)
        m[jset,0] = Msun*1E-30  # give it a tiny mass
        Nhits = Nhits+1
        pos[jset] = (10.*L*Nhits, 0, 0) # put it far away

    Nsteps += 1
