import numpy
from matplotlib import pyplot

c_min = 0.0
c_max = 2.0
tau_min = 0.0
tau_max = 2.0

c_size = 256
tau_size = int(c_size*((tau_max-tau_min)/(c_max-c_min)))

C = numpy.linspace(c_min,c_max,c_size)
TAU = numpy.linspace(tau_min,tau_max,tau_size+1)[1:]

first = numpy.zeros((c_size,tau_size))
second = numpy.zeros((c_size,tau_size))
third = numpy.zeros((c_size,tau_size))

for i in range(c_size):
    for j in range(tau_size):
        c = C[i]
        tau = TAU[j]
        #
        first[i,j] = (tau**2)/((tau-1)**2)
        second[i,j] = first[i,j] + 4*(c-c**2)
        third[i,j] = min(first[i,j],second[i,j])

X,Y = numpy.meshgrid(TAU,C)

minv = 0.9
maxv = 1.1

pyplot.pcolor(X,Y,third,vmin=minv,vmax=maxv,cmap="viridis_r")
pyplot.colorbar()
pyplot.contour(X,Y,second,vmin=minv,vmax=maxv,
               cmap="cool",levels=[1],label="CONDENS-ADVEC")
pyplot.contour(X,Y,third,vmin=minv,vmax=maxv,
               cmap="hot",levels=[1],label="min(CONDENS,CONDENS-ADVEC)")
pyplot.xlabel("Timescale")
pyplot.ylabel("Courant number")
pyplot.title("min(CONDENS,CONDENS+ADVEC)")

pyplot.show(block=False)
