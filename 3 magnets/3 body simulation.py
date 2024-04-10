import pygame
import numpy as np
import turtle


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


def coordinate_converter(x, y):
    a, b = x + int(info.current_w / 2), int(info.current_h / 2) - y
    return a, b



G = 6.67430 * 10 ** (-11) #Universal gravitational constant
step = 0.01 #s

class Object:
    def __init__(self, color, mass, n, x=0, y=0, vy=0, vx=0, ax = 0, ay = 0):
        self.color = color
        self.mass = mass
        self.x = x
        self.y = y
        self.vy = vy
        self.vx = vx
        self.y0 = self.y
        self.x0 = self.x
        self.ax = ax
        self.ay = ay
        self.n = n

    def draw(self):
        self.c = pygame.draw.circle(screen, self.color, (coordinate_converter(self.x, self.y)), 1)


    def calculate_acceleration(self, obj1, obj2):
        d_x1 = obj1.x - self.x
        d_y1 = obj1.y - self.y
        d_1 = np.sqrt (d_x1**2 + d_y1**2)
        alfa1 = np.arctan(d_y1 / d_x1) #in radians

        if self.x <= obj1.x and self.y <= obj1.y:
            Fx1 = G * self.mass * obj1.mass / ((d_1)**2) * np.cos(alfa1)
            Fy1 = G * self.mass * obj1.mass / ((d_1) ** 2) * np.sin(alfa1)
            Ftot1 = np.sqrt(Fx1 ** 2 + Fy1 ** 2)

        elif self.x > obj1.x and self.y <= obj1.y:
            alfa1 = -alfa1
            Fx1 = -G * self.mass * obj1.mass / ((d_1) ** 2) * np.cos(alfa1)
            Fy1 = G * self.mass * obj1.mass / ((d_1) ** 2) * np.sin(alfa1)
            Ftot1 = np.sqrt(Fx1**2 + Fy1**2)

        elif self.x > obj1.x and self.y > obj1.y:
            alfa1 += np.pi
            Fx1 = G * self.mass * obj1.mass / ((d_1) ** 2) * np.cos(alfa1)
            Fy1 = G * self.mass * obj1.mass / ((d_1) ** 2) * np.sin(alfa1)
            Ftot1 = np.sqrt(Fx1**2 + Fy1**2)

        elif self.x < obj1.x and self.y > obj1.y:
            alfa1 = np.pi/2 + alfa1
            Fx1 = G * ((self.mass * obj1.mass) / (d_1 ** 2)) * np.sin(alfa1)
            Fy1 = - G * self.mass * obj1.mass / ((d_1) ** 2) * np.cos(alfa1)
            Ftot1 = np.sqrt(Fx1**2 + Fy1**2)

        d_x2 = obj2.x - self.x
        d_y2 = obj2.y - self.y
        d_2 = np.sqrt(d_x2 ** 2 + d_y2 ** 2)
        alfa2 = np.arctan(d_y2 / d_x2)  # in radians

        if self.x <= obj2.x and self.y <= obj2.y:
            Fx2 = G * self.mass * obj2.mass / ((d_2) ** 2) * np.cos(alfa2)
            Fy2 = G * self.mass * obj2.mass / ((d_2) ** 2) * np.sin(alfa2)
            Ftot2 = np.sqrt(Fx2 ** 2 + Fy2 ** 2)

        elif self.x > obj2.x and self.y <= obj2.y:
            alfa2 = -alfa2
            Fx2 = -G * self.mass * obj2.mass / ((d_2) ** 2) * np.cos(alfa2)
            Fy2 = G * self.mass * obj2.mass / ((d_2) ** 2) * np.sin(alfa2)
            Ftot2 = np.sqrt(Fx2 ** 2 + Fy2 ** 2)

        elif self.x > obj2.x and self.y > obj2.y:
            alfa2 += np.pi
            Fx2 = G * self.mass * obj2.mass / ((d_2) ** 2) * np.cos(alfa2)
            Fy2 = G * self.mass * obj2.mass / ((d_2) ** 2) * np.sin(alfa2)
            Ftot2 = np.sqrt(Fx2 ** 2 + Fy2 ** 2)

        elif self.x < obj2.x and self.y > obj2.y:
            alfa2 = np.pi / 2 + alfa2
            Fx2 = G * ((self.mass * obj2.mass) / (d_2 ** 2)) * np.sin(alfa2)
            Fy2 = - G * self.mass * obj2.mass / ((d_2) ** 2) * np.cos(alfa2)
            Ftot2 = np.sqrt(Fx2 ** 2 + Fy2 ** 2)
        FxTOT = Fx1 + Fx2
        FyTOT = Fy1 + Fy2
        self.ax = FxTOT/self.mass
        self.ay = FyTOT / self.mass


    def update_coordinates(self):
        self.vx += self.ax * step
        self.x += self.vx * step
        self.vy += self.ay * step
        self.y += self.vy * step


B1 = Object(red, 300000000000000, 'B1',x = -20, y = 0, vx = 0, vy = -12.9677865)
B2 = Object(blue, 20000000000000, 'B2',x = 20, y = 0, vx = 0, vy = 7.0322135)
B3 = Object(yellow, 10000000000000, 'B3',x = 35.61344, y = 0, vx = 0, vy = 14.8389335)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run_finished = True
            running = False
            break
    screen.fill(black)
    B1.calculate_acceleration(B2, B3)
    B2.calculate_acceleration(B1, B3)
    B3.calculate_acceleration(B1, B2)
    B1.update_coordinates()
    B2.update_coordinates()
    B3.update_coordinates()
    B1.draw()
    B2.draw()
    B3.draw()
    pygame.display.update()

pygame.quit()
