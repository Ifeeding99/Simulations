import pymunk
import pygame
import matplotlib.pyplot as plt
import numpy as np

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
ball_radius = 10
line_thickness = 1
number_of_balls = 200
time = []
t = 0

def from_pymunk_to_pygame(pos):
    return pos[0], h-pos[1]

class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = vx, vy
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.color = red
        space.add(self.body, self.shape)

    def draw(self):
        x,y = from_pymunk_to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, (x,y), ball_radius)


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


"""with open ('chaos balls.txt', 'w') as f:
    counter = 0
    x = np.random.randint(ball_radius, w-ball_radius)
    y = np.random.randint(ball_radius, h-ball_radius)
    vx = np.random.randint(-600, 600)
    vy = np.random.randint(-600, 600)
    B_written = []
    B_written.append(Ball(x,y,vx,vy))
    while counter < number_of_balls:
        appended = True
        x = np.random.randint(ball_radius, w - ball_radius)
        y = np.random.randint(ball_radius, h - ball_radius)

        for b in B_written:
            if np.sqrt((x-b.x)**2+(y-b.y)**2) <= (ball_radius + 10) :
                appended = False
                break

        if appended == True:
            vx = np.random.randint(-600, 600)
            vy = np.random.randint(-600, 600)
            B_written.append(Ball(x, y, vx, vy))
            counter += 1

    for i in range (number_of_balls):
        f.write(str(B_written[i].x))
        f.write('\n')
        f.write(str(B_written[i].y))
        f.write('\n')
        f.write(str(B_written[i].vx))
        f.write('\n')
        f.write(str(B_written[i].vy))
        f.write('\n')""" #uncomment if you want a new file

list_of_balls = []
with open ('chaos balls.txt', 'r') as f:
    for i in range(number_of_balls):
        #reads the file and creates the balls
        x = int(f.readline())
        y = int(f.readline())
        vx = int(f.readline())
        vy = int(f.readline())
        list_of_balls.append(Ball(x,y,vx,vy))

#creating box
w1 = Wall(0,0,0,h)
w2 = Wall(0,0,w,0)
w3 = Wall(w,h,0,h)
w4 = Wall(w,h,w,0)


#creating the green and blue balls
b1 = Ball(1203,700, 200, -200) #default values are 1200, 700, 200, -200
b1.color = blue
b2 = Ball(100,200, 200, 400) #after 15 s if the blue ball is in the default position the green ball
#will be at approximately (729, 730)
b2.color = green
list_of_balls.append(b1)
list_of_balls.append(b2)
#if you want to check if the 2 special balls aren't overlapping with the others
#comment the line "space.step(1/FPS), time will be frozen and you will be able to see
#if they overlap or not

default_x = []
default_y = []
default_vx = []
default_vy = []  #these are used to get the data of the motion of the second ball with default parameters
#variables are checked for 20 s

value_x = []
value_y = []
value_vx = []
value_vy = []  #these are used to confront the behaviour with standard conditions to a behaviour
#with non-standard conditions


running = True
while running:
    if t < 20:
        time.append(t)
        """default_x.append(b2.body.position[0])
        default_y.append(b2.body.position[1])
        default_vx.append(b2.body.velocity[0])
        default_vy.append(b2.body.velocity[1])""" #uncomment to update the file withe the standard parameters in it
        value_x.append(b2.body.position[0])
        value_y.append(b2.body.position[1])
        value_vx.append(b2.body.velocity[0])
        value_vy.append(b2.body.velocity[1])



    screen.fill(black)
    [ball.draw() for ball in list_of_balls]
    t += 1/FPS
    clock.tick(FPS)
    space.step(1/FPS)
    pygame.display.update()
    mpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                running2 =True
                while running2:
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

pygame.quit()

#writing data obtained by using standard parameters
"""with open ('Chaos balls graph.txt', 'w') as f:
    for i in range(len(default_x)):
        f.write(str(default_x[i]))
        f.write('\n')
        f.write(str(default_y[i]))
        f.write('\n')
        f.write(str(default_vx[i]))
        f.write('\n')
        f.write(str(default_vy[i]))
        f.write('\n')"""


with open ('Chaos balls graph.txt', 'r') as f:
    for i in range(40004 // 4): #40004 is the number of lines in the file
        default_x.append(float(f.readline()))
        default_y.append(float(f.readline()))
        default_vx.append(float(f.readline()))
        default_vy.append(float(f.readline()))

fig, ax = plt.subplots(2,2)
ax[0,0].plot(time, default_x, color = 'red', label = 'default value')
ax[0,0].plot(time, value_x, color = 'blue', label = 'new value')
ax[0,0].set_title('x displacement')
ax[0,0].grid()
ax[0,0].set_xlabel('time(s)')
ax[0,0].set_ylabel('position (pixels)')
ax[0,0].legend(loc = 'upper right')

ax[1,0].plot(time, default_y, color = 'red', label = 'default value')
ax[1,0].plot(time, value_y, color = 'blue', label = 'new value')
ax[1,0].set_title('y displacement')
ax[1,0].grid()
ax[1,0].set_xlabel('time(s)')
ax[1,0].set_ylabel('position (pixels)')
ax[1,0].legend(loc = 'upper right')

ax[0,1].plot(time, default_vx, color = 'red', label = 'default value')
ax[0,1].plot(time, value_vx, color = 'blue', label = 'new value')
ax[0,1].set_title('vx variation')
ax[0,1].grid()
ax[0,1].set_xlabel('time(s)')
ax[0,1].set_ylabel('velocity (pixel/s)')
ax[0,1].legend(loc = 'upper right')

ax[1,1].plot(time, default_vy, color = 'red', label = 'default value')
ax[1,1].plot(time, value_vy, color = 'blue', label = 'new value')
ax[1,1].set_title('vy variation')
ax[1,1].grid()
ax[1,1].set_xlabel('time(s)')
ax[1,1].set_ylabel('velocity (pixel/s)')
ax[1,1].legend(loc = 'upper right')

plt.tight_layout()
plt.show()