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

maxduration = 50.0

res = 120
C_range = numpy.linspace(0,3,res)
Er_range = numpy.linspace(0,3*consts["Dt"],res+1)[1:]

R_settle = numpy.zeros((len(C_range),len(Er_range)))
sethresh = 1e-5

for Ci in range(len(C_range)):
    for Ei in range(len(Er_range)):
        C = C_range[Ci]
        Er = Er_range[Ei]
        #
        c = model_scaled.core(consts,rv,rl,Tf)
        c.u = C * c.Dx / c.Dt
        c.initialise()
        c.Er = Er
        #
        energy_init = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
        energy_prev = energy_init
        #
        while c.t < maxduration:
            c.step()
            energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
            ench = (energy_now - energy_prev) / energy_init
            if c.t > c.Dt and abs(ench) < sethresh:
                break
            energy_prev = energy_now
        #
        if abs(ench) < sethresh:
            R_settle[Ci,Ei] = c.t
        else:
            R_settle[Ci,Ei] = numpy.nan
        #should also check that ench is decreasing over time
    print "done c={0}".format(C_range[Ci])

X,Y = numpy.meshgrid(Er_range,C_range)
RS = numpy.ma.masked_array(R_settle, numpy.isnan(R_settle))
pyplot.pcolor(X,Y,RS)
pyplot.colorbar()
pyplot.title(("First timestep {1}$<t<${2}"+\
              " for which change in total energy variation $<${0}").format(\
                  sethresh,c.Dt,maxduration))
pyplot.xlabel("$E_r$")
pyplot.ylabel("$c$")
pyplot.show(block=False)
