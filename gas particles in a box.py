"""
Press arrow down to move the piston down
Press arrow up to move the piston up
Press spacebar to stop the piston
"""


import pymunk
import pygame
import random
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
FPS = 500
ball_radius = 2
time = []
t = 0
n_of_collisions = []
max_vel = 600
#space.gravity = 0, -981 #uncomment to add gravity
line_thickness = 20


def from_pymunk_to_pygame(pos):
    return pos[0], h-pos[1]

def from_pygame_to_pymunk(pos):
    return pos[0], h - pos[1]

class Particle:
    def __init__(self, x, y):
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = random.randint(-max_vel, max_vel), random.randint(-max_vel, max_vel)
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = 2
        space.add(self.body, self.shape)

    def draw(self):
        x,y = from_pymunk_to_pygame(self.body.position)
        pygame.draw.circle(screen, red, (x,y), ball_radius)

class Wall:
    def __init__(self, xi, yi, xf, yf):
        self.pos_i = [xi, yi]
        self.pos_f = [xf, yf]
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, self.pos_i, self.pos_f, line_thickness)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        xi, yi = from_pymunk_to_pygame(self.pos_i)
        xf, yf = from_pymunk_to_pygame(self.pos_f)
        self.line = pygame.draw.line(screen, white, (xi,yi), (xf,yf), line_thickness)

class Piston:
    def __init__(self, xi, yi, xf, yf):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.pos_i = [xi, yi]
        self.pos_f = [xf, yf]
        self.shape = pymunk.Poly.create_box(self.body, (xf - xi, line_thickness))
        self.body.position = round((xf+xi)/2), round((yf+yi)/2)
        self.shape.elasticity = 1
        self.shape.collision_type = 1
        space.add(self.body, self.shape)
    def draw(self):
        xi, yi = from_pymunk_to_pygame(self.pos_i)
        xf, yf = from_pymunk_to_pygame(self.pos_f)
        x, y = from_pymunk_to_pygame(self.body.position)
        self.rect = pygame.draw.rect(screen, yellow, (xi, yi - (yi - y), xf - xi, line_thickness))

#creating box
lower_x = 300
higher_x = 700
lower_y = 0
higher_y = h - 10

s1 = Piston(lower_x + round(line_thickness/2), higher_y, higher_x - round(line_thickness/2), higher_y)
s2 = Wall(lower_x, lower_y, lower_x, higher_y)
s3 = Wall(lower_x, lower_y, higher_x, lower_y)
s4 = Wall(higher_x, lower_y, higher_x, higher_y)

#creating particles
n_particles = 300
particles = [Particle(random.randint(lower_x+10, higher_x-10), random.randint(lower_y+10, higher_y-10)) for i in range (n_particles)]

#counting collision per second
counter = 0
def count_collision(arbiter, space, data):
    global counter
    counter += 1
handler = space.add_collision_handler(1,2)
handler.post_solve = count_collision

drag = False
running = True
rate = 0.1 #in seconds
next_second = rate #it is used to determine time
#the time is checked every second, if the t variable is equal or greater than
#the next_second variable, the number of collisions is calculated
# and the next_second variable increases by one
#so that the same process can happen the next second
while running:
    screen.fill(black)
    [p.draw() for p in particles]
    s1.draw()
    s2.draw()
    s3.draw()
    s4.draw()
    clock.tick(FPS)
    space.step(1/FPS)
    t += 1/FPS
    #below it is checked when a precise amount of time has passed
    #then the amount of collisions with the piston in that amount of time is registred
    if t > next_second:   #because time is never precisely 1 a small intervall near one is checked
        next_second += rate
        time.append(t)
        n_of_collisions.append(counter)
        counter = 0
    pygame.display.update()
    mpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                s1.body.velocity = 0, -100
            elif event.key == pygame.K_UP:
                s1.body.velocity = 0, 100
            elif event.key == pygame.K_SPACE:
                s1.body.velocity = 0,0


pygame.quit()

plt.plot(time, n_of_collisions, label = 'trend of collisions')
plt.xlabel('time(s)')
plt.ylabel('number of collisions')
plt.grid()
plt.title('Graph of collisions againts the piston')
plt.legend(loc = 'right')
plt.tight_layout()
plt.show()
