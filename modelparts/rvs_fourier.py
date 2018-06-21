import numpy
from scipy import integrate
from matplotlib import pyplot

import get_constants
consts = get_constants.extract("params.txt")
L = consts["L"]
P = consts["P"]

import condens

T_min = condens.T_0
T_max = condens.T_0 + 35

def S_real(T,m):
    Q_s = condens.rvs(T,P)
    return Q_s * numpy.cos(-2*m*T/L)

def S_imag(T,m):
    Q_s = condens.rvs(T,P)
    return Q_s * numpy.sin(-2*m*T/L)

def c(m):
    crd = integrate.quad(S_real, T_min, T_max, args=(m,))
    cid = integrate.quad(S_imag, T_min, T_max, args=(m,))
    return (crd[0]/L, cid[0]/L), (crd[1]/L, cid[1]/L)

modes_to_use = 9

M = range(1,modes_to_use+1)
Cr = []
Ci = []
Ecr = []
Eci = []

for i in range(modes_to_use):
    C,Ec = c(M[i])
    Cr.append(C[0])
    Ci.append(C[1])
    Ecr.append(Ec[0])
    Eci.append(Ec[1])

Qs_Fr = []
Qs_Fi = []
Qs_an = []

Trange = numpy.linspace(T_min,T_max,70)
for T in Trange:
    Qs_Fr.append(sum([Cr[m-1]*numpy.cos(2*numpy.pi*m*T)
                      - Ci[m-1]*numpy.sin(2*numpy.pi*m*T) for m in M]))
    Qs_Fi.append(sum([Ci[m-1]*numpy.cos(2*numpy.pi*m*T)
                      + Cr[m-1]*numpy.sin(2*numpy.pi*m*T) for m in M]))
    Qs_an.append(condens.rvs(T,P))

Trange_even = Trange[::2]
Trange_odd = Trange[1::2]
Qs_Fr_even = Qs_Fr[::2]
Qs_Fr_odd = Qs_Fr[1::2]

pyplot.plot(Trange_even,Qs_Fr_even,label="Fourier numerical, even nodes")
pyplot.plot(Trange_odd,Qs_Fr_odd,label="Fourier numerical, odd nodes")
pyplot.plot(Trange,Qs_an,label="Analytical")
pyplot.legend()
pyplot.show(block=False)
