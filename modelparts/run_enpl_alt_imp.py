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

maxduration = 50.0

C_range = [0.5, 1., 3.]
Er_range = [1./30, 2./30, 0.1, 0.3]

thresh_high = 1.1

spi = 1
for Ci in range(len(C_range))[::-1]:
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
        energy_prev = energy_init
        R_t = [0.0]
        R_energy = [0.0]
        #
        while c.t < maxduration:
            c.step()
            R_t.append(c.t)
            energy_now = (c.vapour ** 2).sum() + (c.liquid ** 2).sum()
            endiff = abs(energy_now - energy_init)/energy_init
            R_energy.append(endiff)
            if c.t > c.Dt and abs(endiff) > thresh_high:
                break
            energy_prev = energy_now
        #
        pyplot.subplot(len(C_range),len(Er_range),spi)
        spi += 1
        pyplot.plot(R_t,R_energy)
        #pyplot.ylim([-0.05,0.05])
        pyplot.title("$c={0}$, $E_r={1}$".format(C,Er))
        #
print "Done"
pyplot.subplots_adjust(left=0.05,bottom=0.05,right=0.99,top=0.95,
                       wspace=0.2,hspace=0.3)
pyplot.show(block=False)
