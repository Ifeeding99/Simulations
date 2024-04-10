import numpy as np
import matplotlib.pyplot as plt

iterations = 200
x = np.array([0.4 for i in range (iterations)])
r = np.linspace(0,4,num = 1000)

for ri in r:
    for i in range(iterations - 1):
        x[i+1] = ri * x[i] * (1 - x[i])

    un = np.unique(x[int(np.round(0.9*iterations)):])
    k = ri * np.ones(len(un))
    plt.plot(k, un, marker='.', markersize = 1, linestyle=' ', color='black', linewidth = 1)
    x = np.array([0.4 for i in range(iterations)])




plt.show()
