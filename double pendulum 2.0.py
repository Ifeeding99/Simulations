"""
This program simulates a double pendulum.
If you want precise simulations adjust the initial conditions before the main while loop.
By pressing spacebar you can move the 2 bodies, but this reduces precision.
At the end of the loop you can plot as many graphs as you want
"""


import pymunk
import pygame
import matplotlib.pyplot as plt
import math

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
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
FPS = 100
space = pymunk.Space()
ball_radius = 10
b1_x = []
b1_y = []
b2_x = []
b2_y = []
time = []

def from_pygame_to_real(l):
    #takes in input pygame coordinates and returns real ones
    #1 pixel = 1 mm
    x = l[0]/1000
    y = (h - l[1]) / 1000
    print("f", " ",x," ",y)
    return x,y

def num_conv(n):
    #one pixels corresponds to 1 mm, converts meters to mm
    #so that pymunk can handle those numbers
    converted = n*1000
    return converted

def num_reconv(n):
    #reconverts pymunk numbers in real numbers
    converted = n/1000
    return converted

def converter_pymunk_to_pygame(pos):
    #takes in input body.position
    return round(pos[0]), round(h - pos[1])

def converter_pygame_to_pymunk(pos):
    #takes in input body.position
    return pos[0], h - pos[1]

g = -9.81
space.gravity = 0, num_conv(g)


class Ball:
    def __init__(self, x, y, mass = 10):
        x = num_conv(x)
        y = num_conv(y)
        self.body = pymunk.Body(mass)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        X,Y = converter_pymunk_to_pygame(self.body.position)
        self.C = pygame.draw.circle(screen, red, (X,Y), ball_radius)


class Attachment_point:
    def __init__(self, x, y):
        x = num_conv(x)
        y = num_conv(y)
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = x, y


class String:
    def __init__(self, b1, b2):
        self.b1 = b1.body
        self.b2 = b2.body
        joint = pymunk.PinJoint(self.b1, self.b2)
        space.add(joint)
        self.lenght = math.sqrt((self.b1.position[0] - self.b2.position[0])**2+(self.b1.position[1] - self.b2.position[1])**2)


    def draw(self):
        x1, y1 = converter_pymunk_to_pygame(self.b1.position)
        x2, y2 = converter_pymunk_to_pygame(self.b2.position)
        pygame.draw.line(screen, white, (x1,y1), (x2,y2), 1)

# parameters
anchor_point = Attachment_point(0.5, 0.4)
b1 = Ball(0.5, 0.3, mass = 0.1)
b2 = Ball(0.5,0.2, mass = 0.1)
string1 = String(anchor_point, b1)
string2 = String(b1, b2)

t = 0
drag = False
running = True
while running:
    screen.fill(black)
    b1.draw()
    b1_x.append(num_reconv(b1.body.position[0]))
    b1_y.append(num_reconv(b1.body.position[1]))

    b2.draw()
    b2_x.append(num_reconv(b2.body.position[0]))
    b2_y.append(num_reconv(b2.body.position[1]))

    string1.draw()
    string2.draw()
    pygame.display.update()
    mpos = pygame.mouse.get_pos()
    clock.tick(FPS)
    space.step(1/FPS)
    t += 1/FPS
    time.append(t)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                running2 = True
                #settings menu
                while running2:
                    screen.fill(black)
                    b1.draw()
                    b2.draw()
                    string1.draw()
                    string2.draw()
                    pygame.display.update()
                    mpos = pygame.mouse.get_pos()
                    clock.tick(FPS)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            running2 = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                                running2 = False
                            elif event.key == pygame.K_SPACE:
                                running2 = False

                        elif event.type == pygame.MOUSEBUTTONDOWN and b1.C.collidepoint(mpos):
                            drag = True
                            while drag:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONUP:
                                        drag = False
                                    else:
                                        screen.fill(black)
                                        c_range = pygame.draw.circle(screen, yellow, (converter_pymunk_to_pygame(anchor_point.body.position)),string1.lenght, 5)
                                        mpos = pygame.mouse.get_pos()
                                        c_mpos = converter_pygame_to_pymunk(mpos)
                                        if c_range.collidepoint(mpos) and (math.sqrt((anchor_point.body.position[0]-c_mpos[0])**2+(anchor_point.body.position[1]-c_mpos[1])**2)) <= string1.lenght+3 and (math.sqrt((anchor_point.body.position[0]-c_mpos[0])**2+(anchor_point.body.position[1]-c_mpos[1])**2)) >= string1.lenght-3:
                                            converted = converter_pygame_to_pymunk(mpos)
                                            incx = converted[0] - b1.body.position[0]
                                            incy = converted[1] - b1.body.position[1]
                                            b1.body.position = converter_pygame_to_pymunk(mpos)
                                            b1.body.velocity = (0,0)
                                            m_a = [b2.body.position[0], b2.body.position[1]]
                                            m_a[0] += incx
                                            m_a[1] += incy
                                            b2.body.position = m_a
                                            b2.body.velocity = (0, 0)
                                        b1.draw()
                                        b2.draw()
                                        string1.draw()
                                        string2.draw()
                                        pygame.display.update()
                                        clock.tick(FPS)



                        elif event.type == pygame.MOUSEBUTTONDOWN and b2.C.collidepoint(mpos):
                            drag = True
                            while drag:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONUP:
                                        drag = False
                                    else:
                                        screen.fill(black)
                                        c_range = pygame.draw.circle(screen, green, (converter_pymunk_to_pygame(b1.body.position)),string2.lenght, 5)
                                        mpos = pygame.mouse.get_pos()
                                        c_mpos = converter_pygame_to_pymunk(mpos)
                                        if c_range.collidepoint(mpos) and (math.sqrt((b1.body.position[0]-c_mpos[0])**2+(b1.body.position[1]-c_mpos[1])**2)) <= string2.lenght+3 and (math.sqrt((b1.body.position[0]-c_mpos[0])**2+(b1.body.position[1]-c_mpos[1])**2)) >= string2.lenght-3:
                                        #if c_range.collidepoint(mpos):
                                            b2.body.position = converter_pygame_to_pymunk(mpos)
                                            b2.body.velocity = (0,0)
                                        b1.draw()
                                        b2.draw()
                                        string1.draw()
                                        string2.draw()
                                        pygame.display.update()
                                        clock.tick(FPS)

pygame.quit()

plt.plot(time, b1_x, marker = '.', color = 'blue', label = 'B1 X')
plt.legend(loc = 'right')
plt.show()