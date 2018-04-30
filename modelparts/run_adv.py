import numpy
from matplotlib import pyplot

import model_ftbs

#need to separate
vu = numpy.linspace(0.0,0.01,9)
for i in range(len(vu)):
    c = model_ftbs.core()
    #initial conditions
    c.u = vu[i]
    c.vapour[:] = 0.01
    c.vapour[int(c.gs*0.25):int(c.gs*0.75)] = 0.99
    c.liquid = (c.vapour * -1.0) + 1.0
    c.E[:] = 0.0
    #
    c.run(100)
    #
    X = numpy.linspace(0.0,c.L,c.gs)
    pyplot.subplot(3,3,i+1)
    pyplot.title("u={0}".format(c.u))
    pyplot.plot(X,c.vapour,label="Water vapour")
    pyplot.plot(X,c.liquid,label="Liquid water")
    #pyplot.legend()
    print "Finished {0} of {1}".format(i+1,len(vu))
pyplot.show(block=False)
