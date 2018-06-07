import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
Tf = numpy.load("temp_field.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_teper
c = model_teper.core(consts,rv,rl,Tf)
c.run(consts["duration"])

X = numpy.linspace(0.0,c.L,c.gs)
pyplot.plot(X,c.vapour)
pyplot.show(block=False)
