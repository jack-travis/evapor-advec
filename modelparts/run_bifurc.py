import numpy
from matplotlib import pyplot
pyplot.rc("font", size=14)

import model_teper
import get_constants

consts = get_constants.extract("params.txt")
Tf = numpy.load("temp_field.npy")
rv = numpy.load("vapour_init.npy")
rl = numpy.load("liquid_init.npy")

from timeit import default_timer as timer
start = timer()

dxdt = (consts["L"]/consts["gs"])/consts["Dt"]
vu = numpy.linspace(0.0,dxdt,128)
vurange = []

for j in range(len(vu)):
    print "U =", vu[j]
    c = model_teper.core(consts,rv,rl,Tf)
    #
    c.u = vu[j]
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
