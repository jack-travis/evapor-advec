import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
re = numpy.load("evapor_condens.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_mcgx
c = model_mcgx.core(consts,rv,rl,re)
c.run(consts["duration"])
