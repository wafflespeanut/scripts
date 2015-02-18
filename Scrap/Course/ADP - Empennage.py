execfile("ADP - Data Collection.py")
execfile("Standard Atmosphere.py")

w0=460719.335414; g=9.81; l=rmin(9)[1]; ar=rmin(1)[1]

wload=rmin(21)[1]; s=(w0*g)/wload
htvc=float(raw_input('Horizontal tail volume coefficient (no unit): '))
cm=float(raw_input('Mean aerodynamic chord (m): '))
dht=float(raw_input('Tail arm ratio (no unit): ')); dht*=l
sht=htvc*cm*s/(dht)
print 'Horizontal tail area: %s m^2'%sht
vtvc=float(raw_input('Vertical tail volume coefficient (no unit): '))
b=(ar*s)**0.5; dvt=0.95*dht; svt=vtvc*b*s/dvt
print 'Vertical tail area: %s m^2'%svt
arht=0.6*ar; print 'Horizontal tail aspect ratio: %s (no unit)'%arht
lamht=float(raw_input('Horizontal tail taper ratio (no unit): '))
bht=(sht*arht)**0.5; print 'Horizontal tail span: %s m'%bht
crht=2*sht/(bht*(lamht+1)); print 'Horizontal tail root chord: %s m'%crht
ctht=lamht*crht; print 'Horizontal tail tip chord: %s m'%ctht
print 'Weight of horizontal tail: %s N'%(0.03*w0*g)
yht=bht*(1+2*lamht)/(6*(1+lamht)); print 'Spanwise location of MAC of horizontal tail: %s m'%yht
cmht=2*crht*(1+lamht+lamht**2)/(3*(lamht+1)); print 'MAC of horizontal tail: %s m'%cmht
arvt=float(raw_input('Vertical tail aspect ratio: %s (no unit)'))
hvt=(arvt*svt)**0.5; print 'Vertical tail height: %s m'%hvt
lamvt=float(raw_input('Vertical tail taper ratio (no unit): '))
crvt=2*svt/(hvt*(lamvt+1)); print 'Vertical tail root chord: %s m'%crvt
ctvt=lamvt*crvt; print 'Vertical tail tip chord: %s m'%ctvt
zvt=2*hvt*(1+2*lamvt)/(6*(1+lamvt)); print 'Spanwise location of MAC of vertical tail: %s m'%zvt
cmvt=2*crvt*(1+lamvt+lamvt**2)/(3*(lamvt+1)); print 'MAC of vertical tail: %s m'%cmvt
print 'Weight of vertical tail: %s N'%(0.02*w0*g)
