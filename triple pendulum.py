import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as smp
from scipy.integrate import odeint

t = smp.symbols('t')
g = smp.symbols('g')
a, b, c = smp.symbols('a b c', cls = smp.Function)
a = a(t)
b = b(t)
c = c(t)

d_a = smp.diff(a, t)
d_b = smp.diff(b, t)
d_c = smp.diff(c, t)

dd_a = smp.diff(d_a, t)
dd_b = smp.diff(d_b, t)
dd_c = smp.diff(d_c, t)

m1, m2, m3 = smp.symbols('m1 m2 m3')
L1, L2, L3 = smp.symbols('L1 L2 L3')

x1 = L1*smp.sin(a)
y1 = L1+L2+L3 - L1*smp.cos(a) # max height is L1 + L2 + L3
x2 = x1 + L2*smp.sin(b)
y2 = y1 - L2*smp.cos(b)
x3 = x2 + L3*smp.sin(c)
y3 = y2 - L3*smp.cos(c)

v1x = smp.diff(x1, t)
v1y = smp.diff(y1, t)
v2x = smp.diff(x2, t)
v2y = smp.diff(y2, t)
v3x = smp.diff(x3, t)
v3y = smp.diff(y3, t)

V = m1*g*y1 + m2*g*y2 + m3*g*y3 #total potential energy
T = (1/2 * m1 * (v1x**2 + v1y**2)) + (1/2 * m2 * (v2x**2 + v2y**2)) + (1/2 * m3 * (v3x**2 + v3y**2)) #total kinetic energy
L = T - V

La = smp.diff((smp.diff(L,d_a)),t) - smp.diff(L,a) #Lagrangian with respect to a (alfa)
Lb = smp.diff((smp.diff(L,d_b)),t) - smp.diff(L,b) #Lagrangian with respect to b (beta)
Lc = smp.diff((smp.diff(L,d_c)),t) - smp.diff(L,c) #Lagrangian with respect to c (gamma)
La.simplify()
Lb.simplify()
Lc.simplify()

sol_dd_a = smp.solve(La, dd_a)
sol_dd_b = smp.solve(Lb, dd_b)
sol_dd_c = smp.solve(Lc, dd_c)


lambd_dz1 = smp.lambdify((t,g,a,b,c,d_a,d_b,d_c, dd_b, dd_c,m1,m2,m3,L1,L2,L3), sol_dd_a)
lambd_dz2 = smp.lambdify((t,g,a,b,c,d_a,d_b,d_c,dd_a,dd_c,m1,m2,m3,L1,L2,L3), sol_dd_b)
lambd_dz3 = smp.lambdify((t,g,a,b,c,d_a,d_b,d_c,dd_a,dd_b,m1,m2,m3,L1,L2,L3), sol_dd_c)
lambd_z1 = smp.lambdify(d_a, d_a)
lambd_z2 = smp.lambdify(d_b, d_b)
lambd_z3 = smp.lambdify(d_c, d_c)

print('value:  ',lambd_z1(1))

#initial parameters:

alfa = np.pi/2
beta = np.pi/2
gamma = 0
d_alfa = 0
d_beta = 0
d_gamma = 0
dd_alfa = 0
dd_beta = 0
dd_gamma = 0
L1 = 1
L2 = 1
L3 = 1
m1 = 1
m2 = 1
m3 = 1
t = np.linspace(0,40,1001)
g = -9.81
x_O = 0 #coordinate x of the pin point
y_O = 0


def dSdt(S, t, m1, m2, m3, L1, L2, L3):
    global dd_alfa
    global dd_beta
    global dd_gamma
    a, z1, b, z2, c, z3 = S
    dd_alfa = lambd_dz1(t,g,a,b,c,z1,z2,z3,dd_beta,dd_gamma,m1,m2,m3,L1,L2,L3)
    dd_alfa = dd_alfa[0]
    dd_beta = lambd_dz2(t, g, a, b, c, z1, z2, z3, dd_alfa, dd_gamma, m1, m2, m3, L1, L2, L3)
    dd_beta = dd_beta[0]
    dd_gamma = lambd_dz3(t, g, a, b, c, z1, z2, z3, dd_alfa, dd_beta, m1, m2, m3, L1, L2, L3)
    dd_gamma = dd_gamma[0]
    d_a = lambd_z1(z1)
    d_b = lambd_z2(z2)
    d_c = lambd_z3(z3)
    d_z1 = lambd_dz1(t,g,a,b,c,z1,z2,z3,dd_beta,dd_gamma,m1,m2,m3,L1,L2,L3)
    d_z2 = lambd_dz2(t,g,a,b,c,z1,z2,z3,dd_alfa,dd_gamma,m1,m2,m3,L1,L2,L3)
    d_z3 = lambd_dz3(t,g,a,b,c,z1,z2,z3,dd_alfa,dd_beta,m1,m2,m3,L1,L2,L3)
    d_z1 = d_z1[0]
    d_z2 = d_z2[0]
    d_z3 = d_z3[0]

    return [d_a,d_z1,d_b,d_z2,d_c,d_z3]


ans = odeint(dSdt, y0 = [alfa, d_alfa, beta, d_beta, gamma, d_gamma], t=t, args = (m1,m2,m3,L1,L2,L3))
for j in ans:
    print(j)

def animate(i):

    alfa, beta, gamma = ans[i,0], ans[i,2], ans[i,4]

    x_alfa = x_O+L1*np.sin(alfa)
    y_alfa = y_O+L1*np.cos(alfa)
    x_beta = x_alfa + L2*np.sin(beta)
    y_beta = y_alfa + L2*np.cos(beta)
    x_gamma = x_beta + L3*np.sin(gamma)
    y_gamma = y_beta + L3*np.cos(gamma)


    plt.clf()
    plt.xlim(-3,3)
    plt.ylim(-3, 3)
    plt.plot(x_alfa, y_alfa, color = 'red', marker = '.', markersize = 10)
    plt.plot(x_beta, y_beta, color='yellow', marker='.', markersize=10)
    plt.plot(x_gamma, y_gamma, color='blue', marker='.', markersize=10)
    plt.plot([x_O, x_alfa], [y_O, y_alfa], color='black') #first string
    plt.plot([x_alfa, x_beta], [y_alfa, y_beta], color='black') #second string
    plt.plot([x_beta, x_gamma], [y_beta, y_gamma], color='black') #third string
    plt.text(2,3, f'tempo:  {t[i]}')
    #print('a:  ', dd_alfa, '   ', d_alfa, '   ',alfa,'\n', 'b:  ', dd_beta, '  ', d_beta, '   ', beta,'\n', 'c:  ', dd_gamma, '   ', d_gamma,'   ', gamma,'\n \n')

ani = FuncAnimation(plt.gcf(), animate, frames = 100, interval = 50, repeat = False)
#ani.save('triple pendulum gif.gif', writer = 'pillow', fps = 1000)
plt.show()
