#Henon studied this fractal while solving a problem about stars orbiting their galactic centre
import matplotlib.pyplot as plt


x = 0.6 #x must not be bigger than 1
y = 0.2
x_cor = []
y_cor = []
for i in range(100000):
    x_cor.append(x)
    y_cor.append(y)
    o_x = x
    x = 1 - 1.5 * (x ** 2) + y #a = 1.4
    y = 0.2 * o_x #b = 0.3

plt.plot(x_cor, y_cor, linestyle='', marker='.', markersize=1)
plt.show()
