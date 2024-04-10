import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sympy as smp

t, mi, l, m, g = smp.symbols('t mi l m g') #uso sympy (symbolic python) anche se non ce n'era vero bisogno, è semplicemente figo
theta = smp.symbols('theta', cls = smp.Function)
theta = theta(t) #theta è funzione del tempo
theta_dot = theta.diff(t) #velocità angolare
theta_double_dot = (-m*g*smp.sin(theta)-mi*theta_dot)/l #calcolo dell'accelerazione angolare
#formula impiegata : a = -mgsin(theta) - mi*v   dove a e v sono accelerazione e velocità angolare
a_acc = smp.lambdify([t, mi, l, m, g, theta, theta_dot], theta_double_dot)
u = smp.lambdify(theta_dot, theta_dot) #serve per risolvere l'equazione differenziale

#parametri iniziali
mi = 0.5
g = 9.81
l = 0.3
m = 1
theta = np.pi*3/2
theta_d = 0

def dSdt(S,t): #funzione che calcola istante per istante accelerazione e velocità angolare
    theta, theta_d = S
    dtheta_dt = u(theta_d)
    dtheta_d_dt = a_acc(t,mi,l,m,g,theta,theta_d)
    return[dtheta_dt, dtheta_d_dt]

t = np.linspace(0,20,1000)
sol = odeint(dSdt, y0 = [theta,theta_d], t = t) #questa è la funzione che approssima la soluzione
angle = []
vel = []
for el in sol: #metto gli angoli e le velocità in due liste separate (prima erano uniti nella lista della soluzione)
    angle.append(el[0])
    vel.append(el[1])

ax = []
for i,el in enumerate(angle): #calcolo quella che è stata l'accelerazione angolare per ogni angolo e la corrispettiva velocità
    a = a_acc(0, mi, l, m, g, el, vel[i])
    ax.append(a)

#grafico
plt.plot(angle,vel, marker = 'x', markersize = 1)
plt.grid()
plt.xlabel('velocità (rad)')
plt.ylabel('accelerazione (rad/s^2)')
plt.show()