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
        self.Er = None
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
        #default Er
        if self.Er is None:
            self.Er = self.Dt * condens.evapor_coeff(self.Tf.mean(),self.P)
    def step(self):
        if self.t <= 0.0:
            self.initialise()
        #first B&F evaporation/condensation,
        for i in range(self.gs):
            Dr = self.Dt*(self.rvs[i] - self.vapour[i])/self.Er
            #apply cap
            Dr = min(Dr, self.liquid[i])
            self.vapour[i] += Dr
            self.liquid[i] -= Dr
        #then advection
        v_n = self.vapour.copy()
        l_n = self.liquid.copy()
        #BTCS advection, solving a matrix equation M*r_new = r_old
        C = self.Dt * self.u / self.Dx
        M = numpy.eye(gs)
        M += numpy.eye(gs, k=1) * C/2
        M += numpy.eye(gs, k=-1) * -C/2
        M[-1,-1] += C/2                     #handles right edge
        v_n[0] += self.initial[0] * C/2     #handles left edge
        l_n[0] += self.initial[1] * C/2     #
        self.vapour = numpy.linalg.solve(a=M, b=v_n)
        self.liquid = numpy.linalg.solve(a=M, b=l_n)
        #OLD BELOW
        #for i in range(self.gs):
        #    drv = v_n[i] - (v_n[i-1] if i > 0 else self.initial[0])
        #    drl = l_n[i] - (l_n[i-1] if i > 0 else self.initial[1])
        #    self.vapour[i] -= self.Dt*(self.u/self.Dx)*drv
        #    self.liquid[i] -= self.Dt*(self.u/self.Dx)*drl
        #finally
        self.t += self.Dt
    def run(self,duration):
        steps = int(float(duration) / self.Dt)
        for _ in range(steps):
            self.step()
#
