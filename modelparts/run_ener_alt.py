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

maxduration = 50

res = 120
C_range = numpy.linspace(0,3,res)
Er_range = numpy.linspace(0,3*consts["Dt"],res+1)[1:]

R_max = numpy.zeros((len(C_range),len(Er_range)))
R_settle = numpy.zeros((len(C_range),len(Er_range)))

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
        endiff_max = 0.0
        #
        #printu = True
        while c.t < maxduration:
            c.step()
            energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
            endiff = abs(energy_now - energy_init) / energy_init
            if endiff_max < endiff:
                endiff_max = endiff
            #elif printu:
            #    print c.t
            #    printu = False
        #
        R_max[Ci,Ei] = endiff_max
        R_settle[Ci,Ei] = endiff
    print "done c={0}".format(C_range[Ci])

X,Y = numpy.meshgrid(Er_range,C_range)

pyplot.subplot(121)
RM = numpy.ma.masked_array(R_max, numpy.isinf(R_max))
RM = numpy.ma.masked_array(RM, numpy.isnan(RM))
pyplot.pcolor(X,Y,RM,vmin=0.,vmax=10.)
pyplot.colorbar()
pyplot.title(("Maximum $L$ achieved for $t<{0}$").format(maxduration))
pyplot.xlabel("$E_r$")
pyplot.ylabel("$c$")

pyplot.subplot(122)
RS = numpy.ma.masked_array(R_settle, numpy.isinf(R_settle))
RS = numpy.ma.masked_array(RS, numpy.isnan(RS))
pyplot.pcolor(X,Y,RS,vmin=0.,vmax=10.)
pyplot.colorbar()
pyplot.title(("$L$ at $t={0}$").format(maxduration))
pyplot.xlabel("$E_r$")
pyplot.ylabel("$c$")

pyplot.show(block=False)
