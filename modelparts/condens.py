import numpy

T_0 = 273.15
B = 0.621859855     #does this vary with temperature?
R_vapour = 461.0    #?
cp_air = 1003.8     #these definitely vary with temperature
cp_vapour = 1885.0  #
cp_liquid = 4186.0  #

def tetens(T):
    T_c = T - T_0
    if T_c < 0:
        return 0.61078*numpy.exp((21.875*T_c)/(T_c+265.5))
    return 0.61078*numpy.exp((17.27*T_c)/(T_c+237.3))

def rvs(T, P):
    e_s = tetens(T)
    return B*e_s/(P-e_s)

def evapor_coeff(T, P):
    L_v = 2.5e6 - (cp_liquid - cp_vapour)*(T - T_0)
    RVS = rvs(T, P)
    return (1 + ((L_v**2)*RVS)/(cp_air*R_vapour*(T**2)))
