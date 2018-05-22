import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
re = numpy.load("evapor_condens.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_mcgx

max_u = consts["L"]/(consts["gs"]*consts["Dt"])

print "Loaded, running simulations"

vu = numpy.linspace(0,max_u,9)
for i in range(len(vu)):
    c = model_mcgx.core(consts,rv,rl,re)
    c.u = vu[i]
    #
    c.run(100)
    #
    X = numpy.linspace(0.0,c.L,c.gs)
    pyplot.subplot(3,3,i+1)
    pyplot.title("u={0}, c={1}".format(c.u, c.u*c.Dt/c.Dx))
    pyplot.plot(X,c.vapour,label="Water vapour")
    pyplot.plot(X,c.liquid,label="Liquid water")
    #pyplot.legend()
    print "Finished {0} of {1}".format(i+1,len(vu))
pyplot.subplots_adjust(left=0.1,bottom=0.1,
                       right=0.9,top=0.9,
                       wspace=0.17,hspace=0.37)
pyplot.show(block=False)
