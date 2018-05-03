import numpy
from matplotlib import pyplot
pyplot.rc("font", size=14)

import model_pare

from timeit import default_timer as timer
start = timer()

vu = numpy.linspace(0.0,0.1,150)
vurange = []

for j in range(len(vu)):
    c = model_pare.core()
    #
    c.u = vu[j]
    c.vapour[:] = 0.00
    c.liquid[:] = 1.00
    c.E[:] = -0.5/c.Dt
    c.E[c.gs/3:int(numpy.round(2.0*c.gs/3))] = 0.5/c.Dt
    #
    c.run(10)
    ratred = c.vapour[int(2*c.gs/3):]
    for i in range(len(ratred)):
        pyplot.plot(vu[j],ratred[i],
                    marker=".",markersize=6,color="k",
                    markerfacecolor=(0,0,0,1.0/9))
pyplot.title("Water vapour concentration in last third of domain,"+
             "\n after 10 time units")
pyplot.xlabel("Background velocity (space/time)")
pyplot.ylabel("Water vapour proportion")
pyplot.subplots_adjust(left=0.06,bottom=0.1,
                       right=0.99,top=0.9)
pyplot.show(block=False)

end = timer()
print end - start
