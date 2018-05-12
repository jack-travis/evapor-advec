import numpy
from matplotlib import pyplot

import model_pare

print "Loaded, running simulation"

c = model_pare.core()
#
c.u = 0.5*c.Dx/c.Dt
c.vapour[:] = 0.00
c.liquid[:] = 1.00
c.E[:] = -0.5/c.Dt
c.E[c.gs/3:int(numpy.round(2.0*c.gs/3))] = 0.5/c.Dt
#
t_ar = [0.0]
v_ar = [c.vapour.copy()]
#
for j in range(1,50):
    c.step()
    t_ar.append(c.t)
    v_ar.append(c.vapour.copy())
    for i in range(len(v_ar[j])):
        if v_ar[j][i] < 0:
            print "time", j, c.t
            print "space", i, float(i)/c.gs
            print v_ar[j-1][i], ">", v_ar[j][i]
            print
#
