import numpy
from matplotlib import pyplot

import model_pare

#need to separate
vu = numpy.linspace(0.0,1.0/9,9)
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
    c.run(70)
    #
    X = numpy.linspace(0.0,c.L,c.gs)
    pyplot.subplot(3,3,i+1)
    pyplot.title("u={0}, c={1}".format(c.u, c.u*c.Dt/c.Dx))
    pyplot.plot(X,c.vapour,label="Water vapour")
    pyplot.plot(X,c.liquid,label="Liquid water")
    #pyplot.legend()
    print "Finished {0} of {1}".format(i+1,len(vu))
pyplot.subplots_adjust(left=0.05,bottom=0.05,
                       right=0.95,top=0.95,
                       wspace=0.15,hspace=0.25)
pyplot.show(block=False)
