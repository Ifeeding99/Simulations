#This is an exercise from the course "Introduction to dynamical systems and chaos" by complexity explorer (Santa Fe university)
#This program plots the Lotka-Volterra attractor given a,b,c,d and the initial conditions
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

iterations = 1000
time = np.linspace(0,100,iterations)

a = 1
b = 1/4
c = 0.2
d = 0.6

def dSdt(S,t):
    r,f = S
    d_r = a*r - b*r*f
    d_f = c*r*f - d*f
    return [d_r,d_f]

sol = odeint(dSdt, y0 = [20,10], t = time)

L_R = []
L_F = []

for el in sol:
    L_R.append(el[0])
    L_F.append(el[1])

fig,ax = plt.subplots(1,3)
ax[0].plot(time,L_R)
ax[0].set_title('rabbit - time graph')
ax[0].grid()

ax[1].plot(time,L_F)
ax[1].set_title('foxes - time graph')
ax[1].grid()

ax[2].plot(L_R,L_F)
ax[2].plot([-100000,100000],[4,4],color = 'red') #red horizontal line (intersects where dR/dt = 0) THIS LINE IS A NULLCLINE (line where derivative is 0)
ax[2].plot([3,3],[-100000,100000], color = 'red') #red vertical line (intersects where dF/dt = 0) THIS LINE IS A NULLCLINE (line where derivative is 0)
ax[2].set_title('rabbit - foxes graph')
ax[2].set_xlim(min(L_R)-2,max(L_R)+2)
ax[2].set_ylim(min(L_F)-2,max(L_F)+2)
ax[2].grid()
plt.show()