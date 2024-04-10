#this model uses Lotka-Volterra equations to model a population of rabbits and foxes
# https://www.youtube.com/watch?v=pDESymjFkAU a video explaining that
# https://www.youtube.com/watch?v=zrFJKy5l_PY  video registred by the MIT on the subject
# https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations  wikipedia link to the subject
# https://www.kristakingmath.com/blog/predator-prey-systems link with explanation

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

t = np.linspace(0, 10000, 10001)

a = 0.002
b = 0.00002
k1 = 0.05
k2 = 0.018


def dSdt(S, t):
    r, f = S
    d_r = k1 * r - a * f * r
    d_f = -k2 * f + b * f * r
    return [d_r, d_f]


sol = odeint(dSdt, y0=[100, 100], t=t)

rabbits = []
foxes = []
for el in sol:
    rabbits.append(el[0])
    foxes.append(el[1])

plt.plot(rabbits, foxes, marker = '.', linestyle = '', markersize = 1)
plt.show()