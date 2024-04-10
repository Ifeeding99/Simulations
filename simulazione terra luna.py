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


def coordinate_converter(x, y):
    a, b = x + int(info.current_w / 2), int(info.current_h / 2) - y
    return a, b



# Earth's mass = 5.972e24
# Moon's mass =
G = 6.67430e-11 #Universal gravitational constant
step = 3600#s


t = 0
posM = {}
time = []
velM = {}
accM = {}
posE = {}
velE = {}
accE = {}
F = []
distance = []
CY = []
CX = []
C_V_X = []
C_V_Y = []
d_E_CM = [] #distance between the Earth and the center of mass of the system

def unit_conversion(n1):
    """200 pixels = earth - moon distance, this function takes in input
    real data and returns the correspondent number of pixels. (1 pixel = 1 962 535 m)"""
    p = (384399e3 + 6371e3 + 1737e3) / 200
    n_p1 = n1 / p
    return n_p1


class Object:
    def __init__(self, color, mass, n, r, x=0, y=0, vy=0, vx=0, ax = 0, ay = 0):
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
        self.r = r

    def draw(self):
        xcor = unit_conversion(self.x)
        ycor = unit_conversion(self.y)
        self.c = pygame.draw.circle(screen, self.color, (coordinate_converter(xcor, ycor)), self.r)


    def calculate_acceleration(self, obj):
        d_x = (obj.x - self.x )
        d_y = (obj.y - self.y)
        d = np.sqrt (d_x**2 + d_y**2)
        alfa = np.arctan(d_y / d_x) #in radians
        if self.x <= obj.x and self.y <= obj.y:
            # 1st quadrant
            Fx = G * self.mass * obj.mass / ((d)**2) * np.cos(alfa)
            Fy = G * self.mass * obj.mass / ((d) ** 2) * np.sin(alfa)
            Ftot = np.sqrt(Fx**2 + Fy**2)
            atot = Ftot/ self.mass
            self.ax = atot * np.cos(alfa)
            self.ay = atot * np.sin(alfa)
            if self.n == 'Moon':
                F.append(Ftot)
                distance.append(d)

        elif self.x > obj.x and self.y <= obj.y:
            #2nd quadrant
            alfa = -alfa
            Fx = -G * self.mass * obj.mass / ((d) ** 2) * np.cos(alfa)
            Fy = G * self.mass * obj.mass / ((d) ** 2) * np.sin(alfa)
            Ftot = np.sqrt(Fx**2 + Fy**2)
            atot = Ftot/ self.mass
            self.ax = - atot * np.cos(alfa)
            self.ay = atot * np.sin(alfa)
            if self.n == 'Moon':
                F.append(Ftot)
                distance.append(d)

        elif self.x > obj.x and self.y > obj.y:
            #3rd quadrant
            alfa += np.pi
            Fx = G * self.mass * obj.mass / ((d) ** 2) * np.cos(alfa)
            Fy = G * self.mass * obj.mass / ((d) ** 2) * np.sin(alfa)
            Ftot = np.sqrt(Fx**2 + Fy**2)
            atot = Ftot/ self.mass
            self.ax = atot * np.cos(alfa)
            self.ay = atot * np.sin(alfa)
            if self.n == 'Moon':
                F.append(Ftot)
                distance.append(d)

        elif self.x < obj.x and self.y > obj.y:
            #4th quadrant
            alfa = np.pi/2 + alfa
            Fx = G * ((self.mass * obj.mass) / (d ** 2)) * np.sin(alfa)
            Fy = - G * self.mass * obj.mass / ((d) ** 2) * np.cos(alfa)
            Ftot = np.sqrt(Fx**2 + Fy**2)
            atot = Ftot/ self.mass
            self.ax = atot * np.sin(alfa)
            self.ay = - atot * np.cos(alfa)
            if self.n == 'Moon':
                F.append(Ftot)
                distance.append(d)


    def update_coordinates(self,t):
        if self.n == 'Moon':
            posM[self.x] = self.y
            time.append(t)
            t += step
            velM[self.vx] = self.vy
            accM[self.ax] = self.ay
        elif self.n == 'Earth':
            posE[self.x] = self.y
            t += step
            velE[self.vx] = self.vy
            accE[self.ax] = self.ay
        self.vx += self.ax*step
        self.vy += self.ay * step
        self.x += self.vx * step
        self.y += self.vy * step
        """if self.n == 'Earth': #uncomment only if you want the Earth to stay at (0,0)
            self.x = 0
            self.y = 0"""
        return t


def calculate_center_of_mass(E:Object, M:Object):
    c_x = (E.mass*E.x + M.mass*M.x) / (E.mass + M.mass)
    c_y = (E.mass*E.y + M.mass*M.y) / (E.mass + M.mass)
    pixel_x, pixel_y = unit_conversion(c_x), unit_conversion(c_y)
    pygame.draw.circle(screen, red, (coordinate_converter(pixel_x, pixel_y)), 1)
    CY.append(c_y)
    CX.append(c_x)
    v_x = (CX[-1] - CX[-2]) / step if len(CX) >= 2 else 0
    v_y = (CY[-1] - CY[-2]) / step if len(CY) >= 2 else 0
    if E.n == 'Earth':
        d_E = np.sqrt((E.y - c_y)**2 + (E.x - c_x)**2)
        d_E_CM.append(d_E)
    C_V_X.append(v_x)
    C_V_Y.append(v_y)



Earth = Object(blue, 5.972e24, 'Earth', 3.246)#Earth's radius in pixels is (6 371 000/ 1 962 535) = 3.246...
Moon = Object(white, 7.34767309e22, 'Moon', 1,x = -(405400.9e3 + 6371e3 + 1737e3),y = 1, vy = 0.97e3)
# the tangent velocity of the Moon is 1023 m/s plus or minus (2pi/2332800*(384399e3 + 6371e3 + 1737e3) (2332800 are the seconds in 27 days)
# the formula used is (2π/ΔT * r)
#Moon's radius in pixels is (1 737 000/ 1 962 535) = 0.885... that is roundest to 1 because
#pygame always rounds to the lowest integer, but 0.885 is closer to 1
#1023 is the average Moon's velocity around the Earth and its average distance from the planet is 384 399 km
#However the Perigee is at 363 228.9 km, the apogee at 405 400 km
#The velocity at the perigee varies between 1.06 and 1.09 km/s
#the velocity at the apogee is 0.97 km/s

z = 0
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
    Earth.calculate_acceleration(Moon)
    Moon.calculate_acceleration(Earth)
    calculate_center_of_mass(Earth, Moon)
    Earth.update_coordinates(z)
    t = Moon.update_coordinates(t)
    Earth.draw()
    Moon.draw()
    pygame.display.update()

pygame.quit()
plt.title('Graph of Moon\'s motion around the Earth')
plt.plot(time, d_E_CM, color = 'blue', linestyle = '', marker = '.', label = 'distance')
plt.legend(loc = 'upper right')
plt.show()


