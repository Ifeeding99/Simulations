"""
This program plots the Loretz attractor in 3D.
The Loretz attractor is the attractor associated with a system of 3 differential equations Loretz studied.
The equations are:
dx/dt = s(y-x)
dy/dt = x(r-z)-y
dz/dt = xy - bz

where s = sigma, r = rho, b = beta
Loretz fixed these parameters to respectively 10, 28, 8/3
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint #to solve the differential equations system

sigma = 10
rho = 28
beta = 8/3

def dSdt(S,t): #function passed to odeint, calculates the derivatives for each time istant
    x, y, z = S #a vector is used for practical reasons: you can return only 1 thing to odeint
    dxdt = sigma*(y-x)
    dydt = x*(rho-z) - y
    dzdt = x*y - beta*z

    return [dxdt, dydt, dzdt] #returns the vector with the derivatives calculated

t = np.linspace(0,40,10000)
X = []
Y = []
Z = []

sol = odeint(dSdt, y0 = [1,1,1], t = t) #it's a multidimensional array, each element has the values of x,y, and z for a specific time instant
for el in sol:
    X.append(el[0])
    Y.append(el[1])
    Z.append(el[2])

ax = plt.axes(projection = '3d')
ax.plot3D(X,Y,Z)
plt.show()