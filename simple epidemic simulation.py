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
pygame.display.set_caption('simple simulation of an epidemic')
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 100
ball_radius = 10
time = []
t = 0
infected = []
healthy = []
immune = []
b_max_vel = 400 #balls max velocity

def from_pymunk_to_pygame(pos):
    return round(pos[0]), round(h - pos[1])

class Ball:
    def __init__(self, x, y, c_t):
        self.infection = False
        self.infection_instant = 0
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = random.randint(-b_max_vel, b_max_vel), random.randint(-b_max_vel, b_max_vel)
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = c_t
        if self.shape.collision_type == 1:
            self.color = red
            self.infection = True
        elif self.shape.collision_type == 2:
            self.color = blue
        else:
            self.color = green
        space.add(self.body, self.shape)

    def draw(self):
        x,y = from_pymunk_to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, (x,y), ball_radius)

    def change_to_red(self, arbiter, space, data):
        if self.color == green:
            self.infection = True
            self.color = red
            self.infection_instant = t
            self.shape.collision_type = 1
        return True

    def change_to_blue(self):
        #the time since having encountered the virus the first time is measured
        #if 2 seconds have passed the individual is not contagious anymore
        #and its color shifts to blue
        if self.infection == True and t > (self.infection_instant+2):
            self.color = blue
            self.infection = False
            self.shape.collision_type = 2



class Segment:
    def __init__(self, xi, yi, xf, yf):
        self.pos_i = (xi, yi)
        self.pos_f = (xf, yf)
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, self.pos_i, self.pos_f, 1)
        self.shape.collision_type = 0
        self.shape.elasticity = 1
        space.add(self.body,self.shape)


n_balls = 100
balls = [Ball(random.randint(0,w), random.randint(0,h), i+3) for i in range (n_balls)]
#adding the initial red ball
b = Ball(random.randint(0,w), random.randint(0,h), 1)
balls.append(b)
#creating box
s1 = Segment (0,0,w,0)
s2 = Segment(0,0,0,h)
s3 = Segment(0,h,w,h)
s4 = Segment(w,h,w,0)
#creating collision handlers
handlers = [space.add_collision_handler(1, i+3) for i in range(n_balls)]
for i, handler in enumerate(handlers):
    handlers[i].begin = balls[i].change_to_red



def count_infected(b):
    counter = 0
    for ball in b:
        if ball.color == red:
            counter += 1
    infected.append(counter)

def count_healthy(b):
    counter = 0
    for ball in b:
        if ball.color == green:
            counter += 1
    healthy.append(counter)

def count_immune(b):
    counter = 0
    for ball in b:
        if ball.color == blue:
            counter += 1
    immune.append(counter)


running = True
while running:
    screen.fill(black)
    count_healthy(balls)
    count_infected(balls)
    count_immune(balls)
    time.append(t)
    [ball.change_to_blue() for ball in balls]
    [ball.draw() for ball in balls]
    clock.tick(FPS)
    space.step(1/FPS)
    t += 1/FPS
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()

plt.plot(time, healthy, color = 'green', label = 'healthy individuals')
plt.plot(time, infected, color = 'red', label = 'infected individuals')
plt.plot(time, immune, color = 'blue', label = 'immune individuals')
plt.title('disease graph')
plt.xlabel('time (s)')
plt.ylabel('n° of individuals')
plt.legend(loc = 'right')
plt.tight_layout()
plt.show()