import numpy
from matplotlib import pyplot

import model_pare

print "Loaded, running simulations"

vu = numpy.linspace(0.0,1.0/9,9)
for j in range(len(vu)):
    c = model_pare.core()
    #
    c.u = vu[j]
    c.vapour[:] = 0.00
    c.liquid[:] = 1.00
    c.E[:] = -0.5/c.Dt
    c.E[c.gs/3:int(numpy.round(2.0*c.gs/3))] = 0.5/c.Dt
    #
    t_ar = [0.0]
    r_ar = [c.vapour/(c.vapour+c.liquid)]
    #
    for _ in range(50):
        c.step()
        t_ar.append(c.t)
        r_ar.append(c.vapour/(c.vapour+c.liquid))
    #
    R = numpy.array(r_ar)
    x_ar = numpy.linspace(0,c.L,c.gs)
    T,X = numpy.meshgrid(t_ar,x_ar)
    pyplot.subplot(3,3,j+1)
    pyplot.title("u={0:.9f} ({1:.9f} Dx/Dt)".format(vu[j],vu[j]*c.Dt/c.Dx))
    pyplot.pcolormesh(T,X,R.transpose(),
                      cmap="inferno",vmin=-1.0,vmax=2.0)
    print "Finished {0} of {1}".format(j+1,len(vu))
#
pyplot.subplots_adjust(left=0.05,bottom=0.05,
                       right=0.95,top=0.95,
                       wspace=0.15,hspace=0.25)
pyplot.show(block=False)
