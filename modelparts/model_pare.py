import numpy

class core:
    #need to "const"ify
    def __init__(self):
        #parameters
        self.L = 1.0
        self.gs = 90
        self.Dt = 0.1
        #derived parameters
        self.Dx = self.L / self.gs
        self.u = (self.Dx / self.Dt)
        #dependents
        self.vapour = numpy.array([0.0]*self.gs)
        self.liquid = numpy.array([0.0]*self.gs)
        self.E = numpy.array([0.0]*self.gs)
        self.t = 0.0
        self.initial = [0.0,0.0]
    def initialise(self):
        self.Dx = self.L / self.gs
        self.initial = [self.vapour[0],self.liquid[0]]
    def step(self):
        if self.t <= 0.0:
            self.initialise()
        #handle i>0
        v_n = self.vapour.copy()
        l_n = self.liquid.copy()
        for i in range(self.gs):
            E_n = self.E[i]
            if E_n > 0.0:
                if l_n[i] < E_n*self.Dt:
                    E_n *= l_n[i]
            if E_n < 0.0:
                if v_n[i] < E_n*self.Dt:
                    E_n *= v_n[i]
            drv = v_n[i] - (v_n[i-1] if i > 0 else self.initial[0])
            drl = l_n[i] - (l_n[i-1] if i > 0 else self.initial[1])
            self.vapour[i] += self.Dt*(+E_n - (self.u/self.Dx)*drv)
            self.liquid[i] += self.Dt*(-E_n - (self.u/self.Dx)*drl)
        self.t += self.Dt
    def run(self,duration):
        steps = int(float(duration) / self.Dt)
        for _ in range(steps):
            self.step()
#
