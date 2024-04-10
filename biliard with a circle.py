import pygame #e questo fu il primo errore
import numpy as np
import matplotlib.pyplot as plt

pygame.init()
info = pygame.display.Info()
w = info.current_w
h = info.current_h
screen = pygame.display.set_mode((w,h), pygame.NOFRAME)
clock = pygame.time.Clock()
step = 0.001
FPS = 1/step
red = (230,50,50)
green = (0, 255, 0)
blue = (0, 0, 128)
brown = (127,64,0)
yellow = (255,255,0)
white = (255, 255, 255)
black = (0,0,0)
violet = (127,0,255)

def unit_conversion(n):
    #takes in input a number in meters and converts it in pixels
    #1000 is the fator of conversion: 1000 pixels = 1m (for this simulation)
    n *= 1000
    return n

def coordinate_converter(x,y):
    b = x + round(info.current_w/2), round(info.current_h/2) - y
    return b


class Ball:
    def __init__(self, x, y, vx, vy, c):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.c = c
        self.radius = 10

    def draw(self):
        c_x = unit_conversion(self.x)
        c_y = unit_conversion(self.y)
        pygame.draw.circle(screen, self.c, (coordinate_converter(c_x,c_y)),self.radius)

    def reflected_on_circle(self):
        if self.x == 0:
            self.vy = -self.vy
        elif self.y == 0:
            self.vx = -self.vx
        else:
            m_tangent_line = -(self.x/self.y)
            m_normal_to_tangent = -(1/m_tangent_line)
            if self.vx == 0:
                m_velocity = 1000000
            else:
                m_velocity = self.vy/self.vx
            alfa = np.arctan(abs(m_normal_to_tangent)) #angle between the normal and the x axis
            theta = np.arctan(abs((m_normal_to_tangent-m_velocity)/(1+m_velocity*m_normal_to_tangent)))#formula for calculating the angle between 2 lines
            #the formula is tan(a)=|(m1-m2)/(1+m1*m2)|
            projected_vector_module = 2*(np.sqrt(self.vx**2+self.vy**2))*np.cos(theta)
            projected_vector_x = projected_vector_module * np.cos(alfa)
            projected_vector_y = projected_vector_module * np.sin(alfa)
            if self.x > 0 and self.y > 0: #first quadrant, the normal vector is pointed to the center of the circle
                projected_vector_x = -projected_vector_x
                projected_vector_y = -projected_vector_y

            elif self.x < 0 and self.y > 0: #second quadrant
                projected_vector_y = -projected_vector_y

            elif self.x < 0 and self.y < 0: #third quadrant
                pass #all components are positive

            elif self.x > 0 and self.y < 0: #fourth quadrant
                projected_vector_x = -projected_vector_x

            self.vx -= projected_vector_x
            self.vy -= projected_vector_y

    def update_position(self):
        self.x += self.vx*step
        self.y += self.vy*step

    def reflected_on_walls(self):
        if self.x >= (w/2000) or self.x <= -(w/2000):
            self.vx = -self.vx
        if self.y >= (h/2000) or self.y <= -(h/2000):
            self.vy = -self.vy


B1 = Ball(0.3,0,-1,-0.5,red)
B2 = Ball(0.300001,0,-1,-0.5,yellow)
r_circ = 0.2
time = []
t = 0
distance = []
B1_x = []
B1_y = []
B1_vx = []
B1_vy = []
B2_x = []
B2_y = []
B2_vx = []
B2_vy = []
d = 0
running = True
while running:
    screen.fill(black)
    B1.draw()
    B2.draw()
    #getting data
    B1_x.append(B1.x)
    B1_y.append(B1.y)
    B1_vx.append(B1.vx)
    B1_vy.append(B1.vy)
    B2_x.append(B1.x)
    B2_y.append(B1.y)
    B2_vx.append(B1.vx)
    B2_vy.append(B1.vy)

    #calcuating distance
    d = np.sqrt((B1.x-B2.x)**2+(B1.y-B2.y)**2)
    distance.append(d)
    time.append(t)
    if np.sqrt(B1.x**2 + B1.y**2)<= r_circ:
        B1.reflected_on_circle()
    if B1.x >= (w/2000) or B1.x <= -(w/2000) or B1.y >= (h/2000) or B1.y <= -(h/2000):
        B1.reflected_on_walls()

    if np.sqrt(B2.x**2 + B2.y**2)<= r_circ:
        B2.reflected_on_circle()
    if B2.x >= (w/2000) or B2.x <= -(w/2000) or B2.y >= (h/2000) or B2.y <= -(h/2000):
        B2.reflected_on_walls()


    B1.update_position()
    B2.update_position()
    pygame.draw.circle(screen, white, (coordinate_converter(0,0)),unit_conversion(r_circ),1)
    pygame.display.update()
    t += step
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()

#fig, ax = plt.subplots(subplot_kw = {'projection' : '3d'}) #if u wanna have fun with 3d
fig, ax = plt.subplots()
ax.plot(time,distance,label='distance between balls') #plots the distance in time between the 2 balls (shows sensitive dependence on initial conditions)
ax.grid()
#ax.plot3D(B1_x,B1_y,B1_vx) #if u wanna have fun with 3d
ax.set_xlabel('time(s)')
ax.set_ylabel('distance(m)')
ax.set_title('distance - time graph')
ax.legend(loc='best')
plt.show()