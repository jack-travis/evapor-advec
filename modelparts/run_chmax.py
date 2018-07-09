import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
Tf = numpy.load("temp_field.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_scaled

max_u = consts["L"]/(consts["gs"]*consts["Dt"])

print "Loaded, running simulations"

C_left = 0.0
C_right = 2.0
TS_left = 0.0
TS_right = 0.2

duration = 20.0
maxcomp = 1e5

square = maxcomp / (duration / consts["Dt"])
tscale = 10 * (TS_right - TS_left)/(C_right - C_left)
basesize = numpy.sqrt(square / tscale)
u_size = int(basesize)
es_size = int(tscale * basesize)

steps = int(duration / consts["Dt"])
print "To do: {0} by {1} by {2} = {3}".format(
    steps,u_size,es_size,steps*u_size*es_size)

C_range = numpy.linspace(C_left,C_right,u_size)
TS_range = numpy.linspace(TS_left,TS_right,es_size+1)[1:]

minergy = numpy.zeros((u_size,es_size))
chrate = numpy.zeros((u_size,es_size))

for j in range(es_size):
    for i in range(u_size):
        c = model_scaled.core(consts,rv,rl,Tf)
        #
        c.u = C_range[i] * c.Dx / c.Dt
        es = TS_range[j] / c.E
        c.E_scale = es
        #
        energy_init = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
        energy_chmin = energy_init
        energy_chrate = numpy.nan
        energy_prev = energy_init
        for _ in range(int(duration/c.Dt)):
            c.step()
            energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
            if energy_chmin > energy_now:
                energy_chmin = energy_now
                energy_chrate = energy_now - energy_prev
            energy_prev = energy_now
        #
        minergy[i,j] = energy_chmin / energy_init
        chrate[i,j] = (energy_chrate / energy_init) / c.Dt
    print "Did {0:.2f}%".format(100.*(j+1)/es_size)

RTS,RC = numpy.meshgrid(TS_range,C_range)
ennan = numpy.ma.masked_where(numpy.isnan(minergy),minergy)
ranan = numpy.ma.masked_where(numpy.isnan(chrate),chrate)
pyplot.subplot(121)
pyplot.title("Minimum proportional kinetic energy")
pyplot.pcolor(RTS,RC,ennan,vmin=0.0,vmax=1.0)
pyplot.colorbar()
pyplot.xlabel("$E_r$")
pyplot.ylabel("$C=u\\Delta t/\\Delta x$")
pyplot.subplot(122)
pyplot.title("Proportional kinetic energy derivative"+\
             "\nat moment of minimum value")
pyplot.pcolor(RTS,RC,ranan,vmin=-0.1,vmax=0.1)
pyplot.colorbar()
pyplot.xlabel("$E_r$")
pyplot.ylabel("$C=u\\Delta t/\\Delta x$")
pyplot.show(block=False)
