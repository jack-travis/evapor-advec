import numpy
from matplotlib import pyplot, cm

sizer = 999

Kr = numpy.linspace(0,1,sizer)
TAU = numpy.linspace(0,1,sizer+1)[1:]

target = 1.0
gamma = (TAU**2)/((TAU-1)**2) - target
for ki in range(sizer):
    K = Kr[ki]
    alpha = -4*K
    beta = 4*K
    C1 = (-beta + numpy.sqrt(beta**2 - 4*alpha*gamma))/(2*alpha)
    C2 = (-beta - numpy.sqrt(beta**2 - 4*alpha*gamma))/(2*alpha)
    pyplot.plot(TAU,C1,c=cm.viridis(K))
    pyplot.plot(TAU,C2,c=cm.viridis(K))
    pyplot.ylim(0,4)
pyplot.xlabel("Condensation timescale")
pyplot.ylabel("Advection Courant number")
pyplot.title("Values of C and $\\tau$ for which |G|=1"
             + "\n for varying K")
pyplot.show(block=False)
