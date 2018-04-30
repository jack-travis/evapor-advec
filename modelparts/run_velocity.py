import numpy
from matplotlib import pyplot

import model_pare

#need to separate
vu = numpy.linspace(0.0,0.1,9)
for i in range(len(vu)):
    c = model_pare.core()
    #initial conditions
    c.u = vu[i]
    c.vapour[:] = 0.0
    c.liquid[:] = 1.0
    #
    #c.vapour[int(c.gs*0.25):int(c.gs*0.5)] = 1.0
    #c.liquid[int(c.gs*0.25):int(c.gs*0.5)] = 0.0
    #c.E[:] = 0.0
    c.E[:] = -0.5/c.Dt
    c.E[c.gs/3:int(numpy.round(2.0*c.gs/3))] = 0.5/c.Dt
    #
    c.run(30)
    #
    X = numpy.linspace(0.0,c.L,c.gs)
    pyplot.subplot(3,3,i+1)
    pyplot.title("u={0}".format(c.u))
    pyplot.plot(X,c.vapour,label="Water vapour")
    pyplot.plot(X,c.liquid,label="Liquid water")
    #pyplot.legend()
    print "Finished {0} of {1}".format(i+1,len(vu))
pyplot.show(block=False)
