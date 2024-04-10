import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
import sympy as smp

t,g,m,k,l = smp.symbols('t g m k l')
r,a = smp.symbols('r a',cls = smp.Function)
r = r(t)
a = a(t)
r_dot = r.diff(t)
a_dot = a.diff(t)
r_double_dot = r_dot.diff(t)
a_double_dot = a_dot.diff(t)

T = 1/2*m*(r_dot**2+((r+l)**2)*a_dot**2)
V = -m*g*(l+r)*smp.cos(a)+1/2*k*r**2

L = T - V
Lr = (smp.diff((smp.diff(L,r_dot)),t) - smp.diff(L,r)).simplify()
La = (smp.diff((smp.diff(L,a_dot)),t) - smp.diff(L,a)).simplify()
sols = smp.solve([Lr,La],(r_double_dot,a_double_dot)) #giusto

ax_r = smp.lambdify([t,g,m,l,k,r,a,r_dot,a_dot],sols[r_double_dot])
ax_a = smp.lambdify([t,g,m,l,k,r,a,r_dot,a_dot],sols[a_double_dot])

v_r = smp.lambdify(r_dot,r_dot)
v_a = smp.lambdify(a_dot,a_dot)

g = -9.81
m = 1
l = 1
k = 100
steps = 1000
t = np.linspace(0,40,steps)
radius = 0.2
alfa = np.pi/3

def dSdt(S,t):
    x,d_x,theta,d_theta = S
    der_x = v_r(d_x)
    der_theta = v_a(d_theta)
    dd_x = ax_r(t,g,m,l,k,x,theta,d_x,d_theta) #-0.2*d_x  #uncomment if u want friction
    dd_theta = ax_a(t, g, m, l, k, x, theta, d_x, d_theta) #-0.2*d_theta  #uncomment if u want friction

    return[der_x,dd_x,der_theta,dd_theta]

solution = odeint(dSdt,y0=[radius,0,alfa,0],t=t)

angle_list = []
vel_angle_list = []
x_list = []
vel_x_list = []

for el in solution:
    x_list.append(el[0])
    vel_x_list.append(el[1])
    angle_list.append(el[2])
    vel_angle_list.append(el[3])



#uncomment if u want to see the animation
def animate(i):
    x = (l+x_list[i])*np.sin(angle_list[i])
    y = (l+x_list[i])*np.cos(angle_list[i])
    plt.clf()
    plt.grid()
    plt.xlim(-2*l,2*l)
    plt.ylim(-2*l,2*l)
    plt.plot(x,y,marker = '.', markersize = 5, color='red')
    plt.plot([0,x],[0,y])
    plt.text (2*l/3,-2*l,f'time: {round(t[i],3)} s')

ani = FuncAnimation(plt.gcf(),animate,frames = steps, interval = 50)
plt.show()


'''
#uncomment if u want phase space
fig,ax = plt.subplots()
ax.plot(x_list,angle_list,linestyle = '-', marker = '.', markersize = 1)
ax.set_title('phase space')
ax.set_xlabel('displacement(m)')
ax.set_ylabel('angle(rad)')
ax.set_xlim(-2,2)
ax.set_ylim(1,5.3)
ax.grid()
plt.show()'''
