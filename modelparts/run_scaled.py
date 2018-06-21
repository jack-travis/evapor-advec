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

duration = 50.0

u_size = 100
es_size = int(u_size * 10 * (TS_right-TS_left)/(C_right-C_left))

steps = int(duration / consts["Dt"])
print "To do: {0} by {1} by {2} = {3}".format(
    steps,u_size,es_size,steps*u_size*es_size)

C_range = numpy.linspace(C_left,C_right,u_size)
TS_range = numpy.linspace(TS_left,TS_right,es_size+1)[1:]

energy = numpy.zeros((u_size,es_size))

for j in range(es_size):
    for i in range(u_size):
        c = model_scaled.core(consts,rv,rl,Tf)
        #
        c.u = C_range[i] * c.Dx / c.Dt
        es = TS_range[j] / c.E
        c.E_scale = es
        #
        energy_init = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
        c.run(duration)
        vap_a = c.vapour.copy()
        liq_a = c.liquid.copy()
        c.step()
        vap_b = c.vapour.copy()
        liq_b = c.liquid.copy()
        #
        energy_a = (vap_a ** 2).sum() + (liq_a ** 2).sum()
        energy_b = (vap_b ** 2).sum() + (liq_b ** 2).sum()
        energy[i,j] = (energy_b - energy_a) / energy_init
    print "Did {0:.2f}%".format(100.*(j+1)/es_size)

RTS,RC = numpy.meshgrid(TS_range,C_range)
pyplot.pcolor(RTS,RC,energy,vmin=-0.01,vmax=0.01,cmap="nipy_spectral")
pyplot.colorbar()
pyplot.xlabel("Condensation timescale")
pyplot.ylabel("Advection courant number")
pyplot.show(block=False)
