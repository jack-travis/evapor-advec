import numpy
from matplotlib import pyplot

class core:
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
    def step(self):
        for i in range(self.gs):
            E_n = self.E[i]
            if E_n > 0.0 and self.liquid[i] <= 0.0:
                E_n = 0.0
            elif self.vapour[i] <= 0.0:
                E_n = 0.0
            drv = self.vapour[i] - self.vapour[i-1]
            drl = self.liquid[i] - self.liquid[i-1]
            self.vapour[i] += self.Dt*(+E_n - (self.u/self.Dx)*drv)
            self.liquid[i] += self.Dt*(-E_n - (self.u/self.Dx)*drl)
        self.t += self.Dt
    def run(self,duration):
        steps = int(float(duration) / self.Dt)
        for _ in range(steps):
            self.step()

du = [1.0,0.8,0.6,0.4,0.2,0.0]
for i in range(len(du)):
    c = core()
    #initial conditions
    c.u *= du[i]
    #
    c.vapour[:] = 1.0
    c.liquid[:] = 0.0
    c.E[:] = -0.5/c.Dt
    c.E[c.gs/3:2*c.gs/3] = 0.5/c.Dt
    #
    c.run(100)
    #
    X = numpy.linspace(0.0,c.L,c.gs)
    pyplot.subplot(2,3,i+1)
    pyplot.title("u={0}".format(c.u))
    pyplot.plot(X,c.vapour,label="Water vapour")
    pyplot.plot(X,c.liquid,label="Liquid water")
    pyplot.legend()
pyplot.show(block=False)
