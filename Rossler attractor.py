#This program displays the Rossler attractor, given the values of the parameters and initial conditions
# wikipedia link: https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

iterations = 10000
time = np.linspace(0,100,iterations)#the differential equations do not depend on time, this is used only to give odeint the number of desired iterations

a = 0.432
b = 2
c = 4

def dSdt(S,t):
    x,y,z = S
    d_x = -y -z
    d_y = x + a*y
    d_z = b + z*(x - c)
    return [d_x, d_y, d_z]

sol = odeint(dSdt, y0 = [0.1,0.1,0.4], t = time) #y0 are the initial conditions, the first is for x, the second for y, the third for z

list_x = []
list_y = []
list_z = []

for el in sol:
    list_x.append(el[0])
    list_y.append(el[1])
    list_z.append(el[2])

ax = plt.axes(projection='3d')
ax.plot3D(list_x,list_y,list_z, linestyle = '', marker = '.', markersize = 1)
plt.show()
