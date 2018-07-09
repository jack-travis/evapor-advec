import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
Tf = numpy.load("temp_field.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_scaled

print "Loaded, running simulations"

import condens
Er_mean = consts["Dt"] * condens.evapor_coeff(Tf.mean(),consts["P"])

C_left = 0.0
C_right = 2.0
Er_left = 0.0
Er_right = Er_mean

duration = 25.0

C_size = 20
Er_size = int(C_size * 10 * (Er_right-Er_left)/(C_right-C_left))

steps = int(duration / consts["Dt"])
print "To do: {0} by {1} by {2} = {3}".format(
    steps,C_size,Er_size,steps*C_size*Er_size)

C_range = numpy.linspace(C_left,C_right,C_size)
Er_range = numpy.linspace(Er_left,Er_right,Er_size+1)[1:]

middle_C = (consts["L"]/consts["gs"])/consts["Dt"]
u_range = [xc * middle_C for xc in C_range]

energy = numpy.zeros((C_size,Er_size))

for j in range(Er_size):
    for i in range(C_size):
        c = model_scaled.core(consts,rv,rl,Tf)
        #
        c.u = u_range[i]
        c.Er = Er_range[j]
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
    print "Did {0:.2f}%".format(100.*(j+1)/Er_size)

REr,Ru = numpy.meshgrid(Er_range,u_range)
ennan = numpy.ma.masked_where(numpy.isnan(energy),energy)
pyplot.pcolor(REr,Ru,ennan,vmin=-5.0,vmax=5.0)
pyplot.colorbar()
pyplot.title("Change in kinetic energy between timesteps {0}~{1}".format(steps,steps+1))
pyplot.xlabel("$E_r$")
pyplot.ylabel("$u$")
pyplot.show(block=False)
