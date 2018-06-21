import numpy
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
Tf = numpy.load("temp_field.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

import model_teper

max_u = consts["L"]/(consts["gs"]*consts["Dt"])

print "Loaded, running simulations"

vu = numpy.linspace(max_u,max_u*1.5,9)
for j in range(len(vu)):
    c = model_teper.core(consts,rv,rl,Tf)
    #
    c.u = vu[j]
    c.liquid = c.vapour.copy()
    #
    t_ar = [0.0]
    r_ar = [c.vapour.copy()]
    #
    for _ in range(300):
        c.step()
        t_ar.append(c.t)
        r_ar.append(c.vapour.copy())
    #
    R = numpy.array(r_ar)
    x_ar = numpy.linspace(0,c.L,c.gs)
    T,X = numpy.meshgrid(t_ar,x_ar)
    pyplot.subplot(3,3,j+1)
    pyplot.title("u={0:.9f} ({1:.9f} Dx/Dt)".format(vu[j],vu[j]*c.Dt/c.Dx))
    pyplot.pcolormesh(T,X,R.transpose(),
                      cmap="inferno",vmin=0.0,vmax=0.02)
    print "Finished {0} of {1}".format(j+1,len(vu))
#
pyplot.subplots_adjust(left=0.07,bottom=0.07,
                       right=0.93,top=0.93,
                       wspace=0.13,hspace=0.27)
pyplot.show(block=False)
