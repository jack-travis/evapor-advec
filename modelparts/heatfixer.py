import numpy
from matplotlib import pyplot

gs = 90
GRACE = float(gs)/6

lower = 10. + 273.15
upper = 20. + 273.15

fix_first = range(0,int(GRACE))
fix_second = range(int(2*GRACE),int(4*GRACE))
fix_third = range(int(5*GRACE),gs)
#fix_first = [0]
#fix_second = [gs/2]
#if gs%2 == 0:
#    fix_second.append((gs/2)-1)
#fix_third = [gs-1]
#

T = numpy.array([lower]*gs)
T[fix_second] = upper

F = 0.1
for _ in range(gs*10):
    T_n = T.copy()
    for j in range(gs):
        T[j] += F*(T_n[(j+1)%gs] - 2*T_n[j] + T_n[j-1])
    #
    T[fix_first] = lower
    T[fix_second] = upper
    T[fix_third] = lower

pyplot.plot(range(gs),T)
pyplot.show(block=False)
