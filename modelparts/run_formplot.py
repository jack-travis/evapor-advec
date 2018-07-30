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

maxduration = 10.0

C_range = [0.5, 1., 3.]
Er_range = [1./30, 2./30, 0.1, 0.3]

sethresh = 1e-5

spi = 1

for Ci in range(len(C_range))[::-1]:
    for Ei in range(len(Er_range)):
        C = C_range[Ci]
        Er = Er_range[Ei]
        #
        c = model_scaled.core(consts,rv,rl,Tf)
        c.u = C * c.Dx / c.Dt
        c.initialise()
        c.Er = Er
        #
        #energy_init = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
        #energy_prev = energy_init
        R_t = [0.0]
        R_vapour = [c.vapour.copy()]
        #
        while c.t < maxduration:
            c.step()
            R_t.append(c.t)
            R_vapour.append(c.vapour.copy())
            #energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
            #ench = (energy_now - energy_prev) / energy_init
            #if c.t > c.Dt and abs(ench) < sethresh:
            #    break
            #energy_prev = energy_now
        #
        RV = numpy.ma.masked_array(R_vapour, numpy.isnan(R_vapour))
        pyplot.subplot(len(C_range),len(Er_range),spi)
        spi += 1
        R_x = numpy.linspace(0,c.L,c.gs)
        T,X = numpy.meshgrid(R_t, R_x)
        Lp = pyplot.pcolormesh(T,X,RV.transpose(),vmin=-0.01,vmax=0.02)
        pyplot.title("$c={0}$, $E_r={1}$".format(C,Er))
        #
print "Done"
cbar_ax = pyplot.axes([0.9,0.1,0.05,0.8])
pyplot.colorbar(Lp, cax=cbar_ax)
pyplot.show(block=False)
