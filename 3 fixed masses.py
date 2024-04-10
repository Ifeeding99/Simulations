import pygame
import numpy as np
import matplotlib.pyplot as plt

pygame.init()
info = pygame.display.Info()
h = info.current_h
w = info.current_w
screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
red = (230, 50, 50)
green = (0, 255, 0)
blue = (0, 0, 128)
brown = (127, 64, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
violet = (127, 0, 255)



height_of_plane = 5
G = 6.67430e-11 #Universal gravitational constant
step = 0.01 #seconds
m_x_position = []
m_y_position = []
v_x = []
v_y = []
a_x = []
a_y = []
time = []


def coordinate_converter(x, y):
    #converts cartesian coordinates in pygame ones
    a, b = x + int(info.current_w / 2), int(info.current_h / 2) - y
    return a, b


def unit_conversion(n1):
    """ 1 pixel = 0.0002645833m
    this function takes in input a number in metres
    and transforms it in pixels"""
    r = 0.0002645833
    n_p = round(n1 / r)
    return n_p

class Body:
    def __init__(self, mass, x, y, color):
        self.mass = mass
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        x_p = unit_conversion(self.x)
        y_p = unit_conversion(self.y)
        pygame.draw.circle(screen, self.color, (coordinate_converter(x_p, y_p)), 2)

    def get_pos(self):
        m_x_position.append(self.x)
        m_y_position.append(self.y)



def calculate_acceleration(M1, m):
    
    d = np.sqrt((M1.x - m.x)**2+(M1.y - m.y)**2+(height_of_plane)**2)
    alfa = np.arctan((M1.y - m.y) / (M1.x - m.x))  # in radians
    
    if m.x <= M1.x and m.y <= M1.y:
        # 1st quadrant
        Fx = G * m.mass * M1.mass / ((d) ** 2) * np.cos(alfa)
        Fy = G * m.mass * M1.mass / ((d) ** 2) * np.sin(alfa)
        Ftot = np.sqrt(Fx ** 2 + Fy ** 2)
        atot = Ftot / m.mass
        ax = atot * np.cos(alfa)
        ay = atot * np.sin(alfa)

    elif m.x > M1.x and m.y <= M1.y:
        # 2nd quadrant
        alfa = -alfa
        Fx = -G * m.mass * M1.mass / ((d) ** 2) * np.cos(alfa)
        Fy = G * m.mass * M1.mass / ((d) ** 2) * np.sin(alfa)
        Ftot = np.sqrt(Fx ** 2 + Fy ** 2)
        atot = Ftot / m.mass
        ax = - atot * np.cos(alfa)
        ay = atot * np.sin(alfa)


    elif m.x > M1.x and m.y > M1.y:
        # 3rd quadrant
        alfa += np.pi
        Fx = G * m.mass * M1.mass / ((d) ** 2) * np.cos(alfa)
        Fy = G * m.mass * M1.mass / ((d) ** 2) * np.sin(alfa)
        Ftot = np.sqrt(Fx ** 2 + Fy ** 2)
        atot = Ftot / m.mass
        ax = atot * np.cos(alfa)
        ay = atot * np.sin(alfa)


    elif m.x < M1.x and m.y > M1.y:
        # 4th quadrant
        alfa = np.pi / 2 + alfa
        Fx = G * ((m.mass * M1.mass) / (d ** 2)) * np.sin(alfa)
        Fy = - G * m.mass * M1.mass / ((d) ** 2) * np.cos(alfa)
        Ftot = np.sqrt(Fx ** 2 + Fy ** 2)
        atot = Ftot / m.mass
        ax = atot * np.sin(alfa)
        ay = - atot * np.cos(alfa)

    return ax, ay

M1, M2, M3 = Body(10**10, 0, 0.05*np.sqrt(3), red), Body(10**10, -0.05, 0, red), Body(10**10, 0.05, 0, red)
m = Body(1, -0.07, 0.03, green)


running = True
vx = 0
vy = 0
t = 0
while running:
    m.get_pos()
    time.append(t)
    v_x.append(vx)
    v_y.append(v_y)
    #a_x.append(ax)
    #a_y.append(ay)
    ax1, ay1 = calculate_acceleration(M1, m)
    ax2, ay2 = calculate_acceleration(M2, m)
    ax3, ay3 = calculate_acceleration(M3, m)
    ax = ax1 + ax2 + ax3
    ay = ay1 + ay2 + ay3
    vx += ax*step
    vy += ay*step
    m.x += vx*step
    m.y += vy*step
    t += step
    screen.fill(black)
    m.draw()
    M1.draw()
    M2.draw()
    M3.draw()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run_finished = True
            running = False
            break

pygame.quit()

plt.plot(time, m_y_position, label = 'y position', marker = '.', color = 'blue', linestyle = ' ')
plt.xlabel('time (s)')
plt.ylabel('position y (m)')
plt.legend()
plt.legend(loc = 'upper right')
plt.title('motion of a body near 3 fixed masses')
plt.show()