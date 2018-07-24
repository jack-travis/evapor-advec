import numpy
from matplotlib import pyplot

Dt = 0.1
L = 1.0
gs = 90
Dx = L/gs

res = 512

k_range = [numpy.pi*float(m)/L for m in range(1,gs)]
R_range = numpy.linspace(0,0.3,res+1)[1:]
c_range = numpy.linspace(0,3,res)

kstable = numpy.zeros((len(R_range),len(c_range)))

for Ri in range(len(R_range)):
    R = R_range[Ri]
    for ci in range(len(c_range)):
        if R == Dt:
            kstable[Ri,ci] = None
        else:
            c = c_range[ci]
            ks_count = 0
            for ki in range(len(k_range)):
                k = k_range[ki]
                first = (1-(Dt / R)) ** 2
                second = 1 + 2*((c**2)-c)*(1-numpy.cos(k*Dx))
                if first*second <= 1:
                    ks_count += 1
            kstable[Ri,ci] = float(ks_count) / len(k_range)

X,Y = numpy.meshgrid(R_range,c_range)

pyplot.title("Proportion of values for $K$ for which system is stable")
pyplot.pcolor(X,Y,kstable.transpose(),cmap="viridis")
pyplot.xlabel("$E_r$")
pyplot.ylabel("$c$")
pyplot.colorbar()
pyplot.show(block=False)
