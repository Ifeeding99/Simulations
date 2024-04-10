import pymunk
import pygame
import numpy as np
import matplotlib.pyplot as plt

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
screen = pygame.display.set_mode((w,h), pygame.NOFRAME)
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 300
ball_radius = 10
wall_radius = 350
number_of_points = 50#half of number of points used as vertices for the poly object in order to approximate a circle
#increasing the number of points too much yields inaccurate simulations
#somewhat of an ideal number of points is 100 or less down to 50
max_velocity = 1000
b1_x = []
b1_y = []
b2_x = []
b2_y = []
time = []
t = 0

def from_pymunk_to_pygame(pos):
    return round(pos[0]), round(h-pos[1])

def from_cartesian_to_pymunk(pos):
    return (pos[0] + w/2,pos[1] + h/2)

x1 = np.linspace(wall_radius, -wall_radius, number_of_points)
x2 = np.linspace(-wall_radius, wall_radius, number_of_points)
y_positive = np.sqrt(wall_radius**2 - x2**2)
y_negative = -np.sqrt(wall_radius**2 - x1**2)
x_vert = np.append(x1,x2)
y_vert = np.append(y_negative, y_positive)
"""fig, ax = plt.subplots()
ax.plot(x_vert, y_vert)
plt.axis('scaled')
plt.show()"""

class Ball:
    def __init__(self, x, y, ct):
        self.body = pymunk.Body()
        self.body.position = from_cartesian_to_pymunk([x,y])
        #self.body.velocity = np.random.randint(-max_velocity, max_velocity+1), np.random.randint(-max_velocity, max_velocity+1)
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = ct
        if self.shape.collision_type == 1:
            self.color = red
        else:
            self.color = yellow
        space.add(self.body, self.shape)

    def draw(self):
        x,y = from_pymunk_to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, (x,y), ball_radius)

class Wall:
    def __init__(self):
        self.bodies = [pymunk.Body(body_type = pymunk.Body.STATIC) for i in range(number_of_points*2 - 1)]
        self.vertices = [from_cartesian_to_pymunk([x_vert[i], y_vert[i]]) for i in range(number_of_points*2)]
        self.a = 0
        self.shapes = [pymunk.Segment(self.bodies[i], (self.vertices[i]),(self.vertices[i+1]), 5) for i in range(number_of_points*2 - 1)]
        for i in range(number_of_points*2 -1):
            self.shapes[i].elasticity = 1
        [space.add(self.bodies[i], self.shapes[i]) for i in range(number_of_points*2-1)]

    def draw(self):
        vertices_conv = [from_pymunk_to_pygame(self.vertices[i]) for i in range (len(self.vertices))]
        pygame.draw.polygon(screen, white, vertices_conv, 5)

def not_collide(arbiter,space,data):
    #this function is passed to the collision handler
    #to ignore collision between the 2 balls
    return False

handler = space.add_collision_handler(1,2)
handler.begin = not_collide

space.gravity = 0, -981
b1 = Ball(20,0,1) #insert some x offset, the measure unit is pixels
b2 = Ball(21,0,2)
w1 = Wall()
running = True
while running:
    screen.fill(black)
    clock.tick(FPS)
    space.step(1/FPS)
    w1.draw()
    b1.draw()
    b2.draw()
    pygame.display.update()
    #adding coordinates to the respective dictionares
    b1_x.append(b1.body.position[0])
    b1_y.append(b1.body.position[1])
    b2_x.append(b2.body.position[0])
    b2_y.append(b2.body.position[1])
    t += 1/FPS
    time.append(t)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


fig = plt.Figure()
fig, ax = plt.subplots(3,1)
ax[0].plot(b1_x, b1_y, color = 'red', label = 'position of ball 1')
ax[0].plot(b2_x, b2_y, color = 'yellow', label = 'position of ball 2')
ax[0].set_title('Chaotic balls')
ax[0].grid()
ax[0].set_xlabel('x (pixels)')
ax[0].set_ylabel('y (pixels)')

ax[1].plot(time, b1_y, color = 'red', label = 'y of ball 1')
ax[1].plot(time, b2_y, color = 'yellow', label = 'y of ball 2')
ax[1].grid()
ax[1].set_title('y position of the balls over time')
ax[1].set_xlabel('time (seconds)')
ax[1].set_ylabel('y (pixels)')

ax[2].plot(time, b1_x, color = 'red', label = 'x of ball 1')
ax[2].plot(time, b2_x, color = 'yellow', label = 'x of ball 2')
ax[2].grid()
ax[2].set_title('x position of the balls over time')
ax[2].set_xlabel('time (seconds)')
ax[2].set_ylabel('x (pixels)')

plt.tight_layout()
plt.show()