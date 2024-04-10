import numpy as np
import matplotlib.pyplot as plt
#from numba import njit

#@njit
def check_if_in_set(C:complex):
    iterations = 50
    z = 0+0j
    for i in range (iterations):
        z = z**2 + C
        M = np.sqrt(z.real**2 + z.imag**2)
        if M > 2:
            return i+1
            break
    if M < 2:
        return iterations


rows = 4000
columns = 4000
values = np.zeros((rows, columns), dtype = 'complex')
graph = np.zeros((rows, columns))
real_lower_bound = -2
real_upper_bound = 1
imaginary_lower_bound = -1.5
imaginary_upper_bound = 1.5



for i in range(rows):
    im_part = imaginary_upper_bound - i*((imaginary_upper_bound - imaginary_lower_bound)/columns)
    values[i] = np.linspace(complex(real_lower_bound, im_part), complex(real_upper_bound,im_part), num = columns, endpoint = True)

for i in range(rows):
    for k in range(columns):
        graph[i,k] = check_if_in_set(values[i,k])



plt.title('The Mandelbrot set')
plt.imshow(graph, cmap = 'viridis', interpolation = 'bilinear', extent = [real_lower_bound, real_upper_bound, imaginary_lower_bound, imaginary_upper_bound])
plt.xlabel = ('real numbers')
plt.ylabel('imaginary numbers')
plt.show()


