import numpy

import condens

class core:
    def __init__(self,constants,rv,rl,Tf):
        #parameters
        self.L = constants["L"]
        self.gs = int(constants["gs"])
        self.Dt = constants["Dt"]
        self.u = constants["u"]
        self.P = constants["P"]
        #derived
        self.Dx = self.L / self.gs
        #dependent
        self.vapour = rv.copy()
        self.liquid = rl.copy()
        self.Tf = Tf.copy()
        self.t = 0.0
        self.initial = [0.0,0.0]
        self.rvs = Tf.copy()    #used as a dummy array
        self.E = Tf.copy()      #
    def initialise(self):
        self.Dx = self.L / self.gs
        self.t = 0.0
        #construct "good" values to use at left edge of grid
        good_rvs = condens.rvs(self.Tf[0],self.P)
        leftsum = self.vapour[0] + self.liquid[0]
        self.initial = [good_rvs,leftsum-good_rvs]
        #
        for i in range(self.gs):
            self.rvs[i] = condens.rvs(self.Tf[i],self.P)
            self.E[i] = condens.evapor_coeff(self.Tf[i],self.P)
    def step(self):
        if self.t <= 0.0:
            self.initialise()
        #first B&F evaporation/condensation,
        for i in range(self.gs):
            vt = self.vapour[i]
            self.vapour[i] += (self.rvs[i] - vt)/self.E[i]
            self.liquid[i] -= (self.rvs[i] - vt)/self.E[i]
        #then FTBS advection
        v_n = self.vapour.copy()
        l_n = self.liquid.copy()
        for i in range(self.gs):
            drv = v_n[i] - (v_n[i-1] if i > 0 else self.initial[0])
            drl = l_n[i] - (l_n[i-1] if i > 0 else self.initial[1])
            self.vapour[i] -= self.Dt*(self.u/self.Dx)*drv
            self.liquid[i] -= self.Dt*(self.u/self.Dx)*drl
        #finally
        self.t += self.Dt
    def run(self,duration):
        steps = int(float(duration) / self.Dt)
        for _ in range(steps):
            self.step()
#
