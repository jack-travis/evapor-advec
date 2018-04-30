import numpy
from matplotlib import pyplot

import model_ftbs

print "Loaded, running simulations"

vu = numpy.linspace(0.0,0.01,9)
for j in range(len(vu)):
    c = model_ftbs.core()
    c.u = vu[j]
    c.vapour[:] = 0.01
    c.vapour[int(c.gs*0.25):int(c.gs*0.75)] = 0.99
    c.liquid = (c.vapour * -1.0) + 1.0
    c.E[:] = 0.0
    t_ar = [0.0]
    r_ar = [c.vapour/(c.vapour+c.liquid)]
    #
    for _ in range(250):
        c.step()
        t_ar.append(c.t)
        r_ar.append(c.vapour/(c.vapour+c.liquid))
    #
    R = numpy.array(r_ar)
    x_ar = numpy.linspace(0,c.L,c.gs)
    T,X = numpy.meshgrid(t_ar,x_ar)
    pyplot.subplot(3,3,j+1)
    pyplot.pcolormesh(T,X,R.transpose(),
                      cmap="inferno",vmin=-1.0,vmax=2.0)
    print "Finished {0} of {1}".format(j+1,len(vu))
pyplot.show(block=False)
