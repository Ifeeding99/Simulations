import numpy as np
import matplotlib.pyplot as plt
import sympy as smp
import time

real_upper_limit = 2
real_lower_limit = -2
imaginary_upper_limit = 2
imaginary_lower_limit = -2
n_in_line = 1000 #the number of samples in a line of the matrix
step = (imaginary_upper_limit-imaginary_lower_limit)/(n_in_line-1) #the step between a number and the next
#1 is subtracted because the extremes are included and the for loop start at i = 0
matrix = np.zeros((n_in_line, n_in_line),dtype = complex)
for i,row in enumerate(matrix):
    matrix[i] = np.linspace(complex(real_lower_limit, imaginary_upper_limit - step* i) ,complex(real_upper_limit, imaginary_upper_limit - step* i),n_in_line) #this line creates the range of all possible complex numbers in each row

def generate_fractal(m):
    return_matrix = np.zeros((n_in_line,n_in_line),dtype=float)
    x = smp.symbols('x')
    f = x ** 3 - 1
    sol = smp.solve(smp.Eq(f, 0))
    n_steps = 10 #number of the repetitions of the method
    df_dx = f.diff(x)
    tot = n_in_line**2
    progress = 0
    for r in range(n_in_line):
        for c in range(n_in_line):
            for i in range(n_steps):
                m[r,c]= m[r,c] - f.evalf(subs={x:m[r,c]})/df_dx.evalf(subs={x:m[r,c]})
                #in Newton's method the next guess is equal to the current guess minus a step
                #the slope of f is its derivative and it's defined as dy/dx
                #dy is f(x) dx is the step
                #solving for the step u obtain step = f(x)/f'(x)
                #so x_next = x - f(x)/f'(x)

            #now I calculate the distances from the roots
            d1 = float(smp.sqrt((m[r,c].real - complex(sol[0]).real)**2+(m[r,c].imag - complex(sol[0]).imag)**2))
            d2 = float(smp.sqrt((m[r,c].real - complex(sol[1]).real)**2+(m[r,c].imag - complex(sol[1]).imag)**2))
            d3 = float(smp.sqrt((m[r,c].real - complex(sol[2]).real)**2+(m[r,c].imag - complex(sol[2]).imag)**2))

            #now I check for the nearest root
            if d1 < d2 and d1 < d3:
                return_matrix[r,c] = 1
            elif d2 < d1 and d2 < d3:
                return_matrix[r,c] = 2
            elif d3 < d1 and d3 < d2:
                return_matrix[r,c] = 3
            else:
                return_matrix[r,c] = 0
                #print(m[r,c].real)

            progress += 1
            print(f'{progress/tot *100} %')

    return return_matrix

image = generate_fractal(matrix)
plt.imshow(image, extent = [real_lower_limit, real_upper_limit,imaginary_lower_limit, imaginary_upper_limit])
plt.title('Newton\'s fractal')
plt.xlabel('real numbers')
plt.ylabel('imaginary numbers')
plt.colorbar(ticks = [0,1,2,3])
plt.show()
print(time.perf_counter())