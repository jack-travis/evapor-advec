import numpy

class core:
    def __init__(self,constants,rv,rl,re):
        #parameters
        self.L = constants["L"]
        self.gs = int(constants["gs"])
        self.Dt = constants["Dt"]
        self.u = constants["u"]
        #derived
        self.Dx = self.L / self.gs
        #dependent
        self.vapour = rv.copy()
        self.liquid = rl.copy()
        self.E = re.copy()
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
        hs = self.Dt / 2
        #first evaporation/condensation,
        for i in range(self.gs):
            E_n = self.E[i]
            #if not enough vapour/liquid is present, reduce E proportionally
            if l_n[i] < E_n*hs:
                E_n = l_n[i]/hs
            if v_n[i] < -E_n*hs:
                E_n = -v_n[i]/hs
            #is this really correct?
            self.vapour[i] += hs*E_n
            self.liquid[i] -= hs*E_n
        #then advection
        for i in range(self.gs):
            drv = v_n[i] - (v_n[i-1] if i > 0 else self.initial[0])
            drl = l_n[i] - (l_n[i-1] if i > 0 else self.initial[1])
            self.vapour[i] -= hs*(self.u/self.Dx)*drv
            self.liquid[i] -= hs*(self.u/self.Dx)*drl
        self.t += self.Dt
    def run(self,duration):
        steps = int(float(duration) / self.Dt)
        for _ in range(steps):
            self.step()
#
