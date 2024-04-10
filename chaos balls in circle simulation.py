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
screen = pygame.display.set_mode((w,h),pygame.NOFRAME)
pygame.display.set_caption("Chaos balls in a circle simulation")
clock = pygame.time.Clock()
g = -9.81
step = 0.0003 #seconds, 0.0005 is ideal, 0.0003 too, in general, the lower the better
FPS = 1/step
circle_radius = 1 #meters
#conversion: 350 pixels = 1 m
time = []
t = 0
b1_x = []
b1_y = []
b2_x = []
b2_y = []
b1_vx = []
b2_vx = []
b1_vy = []
b2_vy = []

def coordinate_converter(x,y):
    b = x + int(info.current_w/2), int(info.current_h/2) - y
    return b

def unit_conversion(n):
    #takes in input a number in meters and converts it in pixels
    #350 is the fator of conversion
    n *= 350
    return n

class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.ball_radius = 10
        self.internal_time = 0
        self.x0 = x
        self.y0 = y
        self.v0x = vx
        self.v0y = vy

    def Euler_update_coordinates(self):
        #updates the coordinates using Euler's method to approximate
        self.vy += g * step
        self.x += self.vx * step
        self.y += self.vy * step


    def Analytic_update_coordinates(self):
        #updates coordinates using the analytic method ( y = y0 + v0y*t + 1/2*a*t^2)
        self.internal_time += step
        self.vy = self.v0y + g * self.internal_time
        self.y = self.y0 + self.v0y * self.internal_time + (1/2) * g * (self.internal_time)**2
        self.x = self.x0 + self.v0x * self.internal_time



    def collision(self, P):
        if P[0] == 0:
            self.vy = -self.vy
        elif P[1] == 0:
            self.vx = -self.vx
        else:
            #calculates the reflected velocity vector given the point of collision
            m_tangent_line = -(P[1]/P[0])
            #the derivative of a circle centered ad 0,0 is -(x/y)
            m_normal = -m_tangent_line
            #the m of the normal to a line is m of the line * (-1)
            alfa = np.arctan(abs(m_normal))
            #alfa is the angle between the x axis and the normal
            #the m of a line is equal to the tangent of the angle between the line and the x axis
            if self.vx == 0:
                m_current_velocity = 1000000 #a big number is used to approximate the m of the y axis
            else:
                m_current_velocity = self.vy / self.vx
            #this is the m of the vector representing current velocity
            theta = np.arctan(abs((m_current_velocity - m_normal)/ (1 + m_current_velocity*m_normal)))
            #theta is the angle between the vector and the normal
            #it is calculated using the formula that tells the angle between two lines given the ms
            #the formula is      tan(theta) = |(m1 - m2)/(1+m1*m2)|
            projected_vector_module = np.sqrt(self.vy**2 + self.vx**2) * np.cos(theta)
            #this is the module of the projection of the velocity vector on the normal
            projected_vector_module *= 2
            #because you have to subtract 2 * the projection on the normal
            projected_vector_x = projected_vector_module * np.cos(alfa)
            projected_vector_y = projected_vector_module * np.sin(alfa)
            #now I calculated the components of the normal vector
            #now I check in which quadrant the collision happened to assign the sign to the projected vetor components
            if P[0] > 0 and P[1] > 0: #first quadrant, the normal vector is pointed to the center of the circle
                projected_vector_x = -projected_vector_x
                projected_vector_y = -projected_vector_y

            elif P[0] < 0 and P[1] > 0: #second quadrant
                projected_vector_y = -projected_vector_y

            elif P[0] < 0 and P[1] < 0: #third quadrant
                pass #all components are positive

            elif P[0] > 0 and P[1] < 0: #fourth quadrant
                projected_vector_x = -projected_vector_x

            #now to get the reflected velocity vector I sum the components of the normal vector and the current velocity vector
            self.vx += projected_vector_x
            self.vy += projected_vector_y

        #now the lines for the analytic previsions come
        self.internal_time = 0
        self.y0 = self.y
        self.v0y = self.vy
        #self.v0y = 5.81242
        self.x0 = self.x
        self.v0x = self.vx




    def draw(self):
        pix_x = round(unit_conversion(self.x))
        pix_y = round(unit_conversion(self.y))
        conv_pos = coordinate_converter(pix_x, pix_y)
        self.ball = pygame.draw.circle(screen, self.color, conv_pos, self.ball_radius)


b1 = Ball(0.01,0.75,0,0, red)
b2 = Ball(0.01001,0.75,0,0, yellow)

def update_lists():
    b1_x.append(b1.x)
    b2_x.append(b2.x)
    b1_y.append(b1.y)
    b2_y.append(b2.y)
    b1_vx.append(b1.vx)
    b2_vx.append(b2.vx)
    b1_vy.append(b1.vy)
    b2_vy.append(b2.vy)

running = True
while running:
    screen.fill(black)
    update_lists()
    b1.Analytic_update_coordinates()
    b2.Euler_update_coordinates()
    time.append(t)
    C = pygame.draw.circle(screen, white, coordinate_converter(0,0), unit_conversion(1), 1)
    b1.draw()
    b2.draw()
    d1 = np.sqrt(b1.x**2 + b1.y**2)
    d1 = unit_conversion(d1)
    if d1 >= (unit_conversion(circle_radius) - b1.ball_radius):
        point = [b1.x, b1.y]
        b1.collision(point)

    d2 = np.sqrt(b2.x ** 2 + b2.y ** 2)
    d2 = unit_conversion(d2)

    if d2 >= (unit_conversion(circle_radius) - b1.ball_radius):
        point = [b2.x, b2.y]
        b2.collision(point)
    clock.tick(FPS)
    pygame.display.update()
    t += step
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()

fig, ax = plt.subplots(2,2)
ax[0,0].plot(time, b1_x, color = 'red', label = 'B 1')
ax[0,0].plot(time, b2_x, color = 'yellow', label = 'B 2')
ax[0,0].grid()
ax[0,0].set_title('x over time')
ax[0,0].legend()

ax[0,1].plot(time, b1_y, color = 'red', label = 'B 1')
ax[0,1].plot(time, b2_y, color = 'yellow', label = 'B 2')
ax[0,1].grid()
ax[0,1].set_title('y over time')
ax[0,1].legend()

ax[1,0].plot(time, b1_vx, color = 'red', label = 'B 1')
ax[1,0].plot(time, b2_vx, color = 'yellow', label = 'B 2')
ax[1,0].grid()
ax[1,0].set_title('vx over time')
ax[1,0].legend()

ax[1,1].plot(time, b1_vy, color = 'red', label = 'B 1')
ax[1,1].plot(time, b2_vy, color = 'yellow', label = 'B 2')
ax[1,1].grid()
ax[1,1].set_title('vy over time')
ax[1,1].legend()

plt.tight_layout()
plt.show()