import pygame
import numpy as np
from numba import njit


pygame.init()
red = (230,50,50)
green = (0, 255, 0)
blue = (0, 0, 128)
brown = (127,64,0)
yellow = (255,255,0)
white = (255, 255, 255)
black = (0,0,0)
violet = (127,0,255)
info = pygame.display.Info()
w = info.current_w
h = info.current_h
screen = pygame.display.set_mode((w,h),pygame.NOFRAME)
#screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Mandelbrot set zoom")




real_lower_limit = -3
real_upper_limit = 1
imaginary_lower_limit = -1.5
imaginary_upper_limit = 1.5
iterations = 50

def coordinate_converter(n:complex):
    #converts from imaginary numbers to coordinates in the pygame plane
    step_x = abs((real_upper_limit - real_lower_limit))/w
    step_y = abs((imaginary_upper_limit - imaginary_lower_limit) / h)
    x_cor = float(n.real - ((real_upper_limit + real_lower_limit)/2))
    y_cor = float(n.imag - ((imaginary_upper_limit + imaginary_lower_limit)/2))

    x = round(w/2 + x_cor/step_x)
    y = round(h/2 - y_cor/step_y)
    return x,y


def number_converter(x,y):
    #converts from pygame coordinates in imaginary numbers
    step_x = abs((real_upper_limit - real_lower_limit))/w
    step_y = abs((imaginary_upper_limit - imaginary_lower_limit) / h)
    R = real_lower_limit + x * step_x
    y = h - y
    I = imaginary_lower_limit + y * step_y
    n = complex(R,I)
    return n


def check_if_in_set(C:complex):
    z = 0+0j
    for i in range (iterations):
        z = z**2 + C
        M = np.sqrt(z.real**2 + z.imag**2)
        if M > 2:
            return i+1
            break
    if M <= 2:
        return iterations


def get_numbers(rll, rul, ill, iul):
    #takes in input real lower limit, real upper limit, imaginary lower limit, imaginary upper limit
    num = np.zeros((h,w),dtype = 'complex')
    step_i = (iul - ill) / h
    step_r = (rul - rll) / w
    for i in range(h):
        for k in range(w):
            num[i,k] = complex(rll + k * step_r, ill + i * step_i)
    return num

def color(n:complex, iter):
    #takes in input the complex number and the number of iterations
    n_col = int(255/iterations) * iter
    x_cor, y_cor = coordinate_converter(n)
    screen.set_at((int(x_cor), int(y_cor)), (n_col, n_col, n_col))#uncomment this if you want multiple shades of color

    """if iter == iterations:
        col = white
    else:
        col = black
    x_cor, y_cor = coordinate_converter(n)
    screen.set_at((int(x_cor), int(y_cor)), col)""" #uncomment this if you want to use more than 250 iterations (2 colors: black and white)



screen.fill(black)
numbers = get_numbers(real_lower_limit, real_upper_limit, imaginary_lower_limit, imaginary_upper_limit)
print(numbers.shape)

counter = 0
total_numbers = w * h
for i in range(numbers.shape[0]):
    for k in range(numbers.shape[1]):
        it = check_if_in_set(numbers[i,k])
        color(numbers[i,k], it)
        counter += 1
        print(counter / total_numbers *100, " ", "%")



print('Done')
running = True
mouse_clicks = 0
new_4_numbers = []
while running:
    mpos = pygame.mouse.get_pos()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicks += 1
            z = number_converter(mpos[0], mpos[1])
            new_4_numbers.append(z)
            pygame.draw.circle(screen, red, (mpos[0], mpos[1]),2)
            if len(new_4_numbers) == 4:
                pygame.display.update()
                imaginary_upper_limit = max([new_4_numbers[i].imag for i in range(4)])
                imaginary_lower_limit = min([new_4_numbers[i].imag for i in range(4)])
                real_upper_limit = max([new_4_numbers[i].real for i in range(4)])
                real_lower_limit = min([new_4_numbers[i].real for i in range(4)])
                mouse_clicks = 0
                new_4_numbers = []

                screen.fill(black)
                numbers = get_numbers(real_lower_limit, real_upper_limit, imaginary_lower_limit, imaginary_upper_limit)
                counter = 0
                for i in range(h):
                    for j in range(w):
                        it = check_if_in_set(numbers[i, j])
                        color(numbers[i, j], it)
                        counter += 1
                        print(counter / total_numbers * 100, " ", "%")
                print('Done')



pygame.quit()