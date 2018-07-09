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

duration = 30.0
C = 1.0
Er = 0.04

c = model_scaled.core(consts,rv,rl,Tf)
#
c.u = C * c.Dx / c.Dt
es = Er / c.E
c.E_scale = es
#
energy_init = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
energy_prev = energy_init
#
steps = int(duration / c.Dt)
T = [0.0]
Echr = [0.0]
for _ in range(steps):
    c.step()
    energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
    Echr.append((energy_now - energy_prev) / energy_init)
    T.append(c.t)
    energy_prev = energy_now
#
pyplot.plot(T,Echr)
pyplot.ylim([-5,5])
pyplot.show(block=False)
