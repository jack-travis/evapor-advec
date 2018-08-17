import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
Tf = numpy.load("temp_field.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_implicit

max_u = consts["L"]/(consts["gs"]*consts["Dt"])

print "Loaded, running simulations"

maxduration = 100

res = 12
C_range = numpy.linspace(0,3,res)
Er_range = numpy.linspace(0,3*consts["Dt"],res+1)[1:]

R_settle = numpy.zeros((len(C_range),len(Er_range)))

for Ci in range(len(C_range)):
    for Ei in range(len(Er_range)):
        C = C_range[Ci]
        Er = Er_range[Ei]
        #
        c = model_implicit.core(consts,rv,rl,Tf)
        c.u = C * c.Dx / c.Dt
        c.initialise()
        c.Er = Er
        #
        energy_init = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
        endiff_max = 0.0
        #
        printu = True
        while c.t < maxduration:
            c.step()
            energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
            endiff = abs(energy_now - energy_init) / energy_init
            if endiff_max < endiff:
                endiff_max = endiff
            elif printu:
                print c.t
                printu = False
        #
        R_settle[Ci,Ei] = endiff_max
    print "done c={0}".format(C_range[Ci])

X,Y = numpy.meshgrid(Er_range,C_range)
RS = numpy.ma.masked_array(R_settle, numpy.isnan(R_settle))
pyplot.pcolor(X,Y,RS)
pyplot.colorbar()
pyplot.title(("Maximum $L$ (?) achieved for $t<{0}$").format(maxduration))
pyplot.xlabel("$E_r$")
pyplot.ylabel("$c$")
pyplot.show(block=False)
