import numpy
from matplotlib import pyplot
pyplot.rc("font", size=14)

import get_constants

consts = get_constants.extract("params.txt")
Tf_flat = numpy.load("temp_field.npy")
Tf_sharp = numpy.load("temp_triang.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

Tfields = [Tf_flat,Tf_sharp]
titles = ["Square","Triangular"]

import model_teper

for i in range(2):
    c = model_teper.core(consts,rv,rl,Tfields[i])
    c.run(consts["duration"])
    pyplot.subplot(1,2,i+1)
    X = numpy.linspace(0.0,c.L,c.gs)
    pyplot.plot(X,c.vapour)
    pyplot.title(titles[i])
    pyplot.xlabel("Space")
    if i == 0:
        pyplot.ylabel("Vapour concentration")
#
pyplot.suptitle("Effect of temperature field on steady state")
pyplot.subplots_adjust(left=0.09,bottom=0.09,
                       right=0.99,top=0.89,
                       wspace=0.15)
pyplot.show(block=False)
