import pygame
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
screen = pygame.display.set_mode((w,h),pygame.NOFRAME)
pygame.display.set_caption("Chaos balls in a circle simulation")
clock = pygame.time.Clock()
step = 0.001
FPS = 1/step
F = 5 #absolute magnetic force
delta_z = 0 #distance of the plane of the moving mass from the magnets



def coordinate_converter(x,y):
    b = x + round(info.current_w/2), round(info.current_h/2) - y
    return b


def unit_conversion(n):
    #takes in input a number in meters and converts it in pixels
    #350 is the factor of conversion, so 1m = 350 pixels
    n *= 350
    return n

class Magnet:
    def __init__(self, x, y, color ,force = F):
        self.x = x
        self.y = y
        self.color = color
        self.F = F
        self.magnet_radius = 0.06 # meters

    def draw(self):
        x_pix, y_pix = unit_conversion(self.x), unit_conversion(self.y)
        pos = coordinate_converter(x_pix, y_pix)
        rad = unit_conversion(self.magnet_radius)
        self.circle = pygame.draw.circle(screen, black, pos, rad,2)


class Ball:
    def __init__(self, x, y, mass = 1,vx = 0, vy = 0):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.ball_radius = 3
        self.color = white

    def draw(self):
        x_pix, y_pix = unit_conversion(self.x), unit_conversion(self.y)
        pos = coordinate_converter(x_pix, y_pix)
        self.circle = pygame.draw.circle(screen, self.color, pos, self.ball_radius)


    def calculate_acceleration_squared(self, m1, m2, m3):
        d1x = np.absolute(self.x - m1.x)
        d1y = np.absolute(self.y - m1.y)
        d1_plane = np.sqrt((d1x) ** 2 + (d1y) ** 2)
        d1 = np.sqrt((d1x) ** 2 + (d1y) ** 2 + delta_z ** 2)
        if delta_z != 0:
            theta1 = np.arctan(d1_plane / delta_z)
            F1 = (F / d1**2) * np.sin(theta1)  # component of the force on the plane
        else:
            F1 = F / d1**2
        if d1x != 0:
            alfa1 = np.arctan(d1y / d1x)  # angle of the distance vector
        else:
            alfa1 = np.pi / 2  # 90° in radiants
        F1x = F1 * np.cos(alfa1)
        F1y = F1 * np.sin(alfa1)
        a1x = F1x / self.mass
        a1y = F1y / self.mass
        if self.x >= m1.x:  # checking the sign of the acceleration
            a1x = - a1x
        if self.y >= m1.y:
            a1y = -a1y

        d2x = np.absolute(self.x - m2.x)
        d2y = np.absolute(self.y - m2.y)
        d2_plane = np.sqrt((d2x) ** 2 + (d2y) ** 2)
        d2 = np.sqrt((d2x) ** 2 + (d2y) ** 2 + delta_z ** 2)
        if delta_z != 0:
            theta2 = np.arctan(d2_plane / delta_z)
            F2 = (F / d2**2) * np.sin(theta2)  # component of the force on the plane
        else:
            F2 = F / d2**2
        if d2x != 0:
            alfa2 = np.arctan(d2y / d2x)  # angle of the distance vector
        else:
            alfa2 = np.pi / 2
        F2x = F2 * np.cos(alfa2)
        F2y = F2 * np.sin(alfa2)
        a2x = F2x / self.mass
        a2y = F2y / self.mass
        if self.x >= m2.x:  # checking the sign of the acceleration
            a2x = - a2x
        if self.y >= m2.y:
            a2y = -a2y

        d3x = np.absolute(self.x - m3.x)
        d3y = np.absolute(self.y - m3.y)
        d3_plane = np.sqrt((d3x) ** 2 + (d3y) ** 2)
        d3 = np.sqrt((d3x) ** 2 + (d3y) ** 2 + delta_z ** 2)
        if delta_z != 0:
            theta3 = np.arctan(d3_plane / delta_z)
            F3 = (F / d3**2) * np.sin(theta3)  # component of the force on the plane
        else:
            F3 = F / d3**2
        if d3x != 0:
            alfa3 = np.arctan(d3y / d3x)  # angle of the distance vector
        else:
            alfa3 = np.pi / 2
        F3x = F3 * np.cos(alfa3)
        F3y = F3 * np.sin(alfa3)
        a3x = F3x / self.mass
        a3y = F3y / self.mass
        if self.x >= m3.x:  # checking the sign of the acceleration
            a3x = - a3x
        if self.y >= m3.y:
            a3y = -a3y

        # sum of all the accelerations
        self.ax = a1x + a2x + a3x
        self.ay = a1y + a2y + a3y




    def calculate_acceleration(self, m1, m2, m3):
        d1x = np.absolute(self.x - m1.x)
        d1y = np.absolute(self.y - m1.y)
        d1_plane = np.sqrt((d1x) ** 2 + (d1y) ** 2)
        d1 = np.sqrt((d1x)**2 + (d1y)**2 + delta_z**2)
        if delta_z != 0:
            theta1 = np.arctan(d1_plane / delta_z)
            F1 = (F / d1) * np.sin(theta1) #component of the force on the plane
        else:
            F1 = F / d1
        if d1x != 0:
            alfa1 = np.arctan(d1y / d1x) #angle of the distance vector
        else:
            alfa1 = np.pi / 2 #90° in radiants
        F1x = F1 * np.cos(alfa1)
        F1y = F1 * np.sin(alfa1)
        a1x = F1x / self.mass
        a1y = F1y / self.mass
        if self.x >= m1.x: #checking the sign of the acceleration
            a1x = - a1x
        if self.y >= m1.y:
            a1y = -a1y

        d2x = np.absolute(self.x - m2.x)
        d2y = np.absolute(self.y - m2.y)
        d2_plane = np.sqrt((d2x) ** 2 + (d2y) ** 2)
        d2 = np.sqrt((d2x)**2 + (d2y)**2 + delta_z**2)
        if delta_z != 0:
            theta2 = np.arctan(d2_plane / delta_z)
            F2 = (F / d2) * np.sin(theta2) #component of the force on the plane
        else:
            F2 = F / d2
        if d2x != 0:
            alfa2 = np.arctan(d2y / d2x) #angle of the distance vector
        else:
            alfa2 = np.pi / 2
        F2x = F2 * np.cos(alfa2)
        F2y = F2 * np.sin(alfa2)
        a2x = F2x / self.mass
        a2y = F2y / self.mass
        if self.x >= m2.x:  # checking the sign of the acceleration
            a2x = - a2x
        if self.y >= m2.y:
            a2y = -a2y

        d3x = np.absolute(self.x - m3.x)
        d3y = np.absolute(self.y - m3.y)
        d3_plane = np.sqrt((d3x) ** 2 + (d3y) ** 2)
        d3 = np.sqrt((d3x)**2 + (d3y)**2 + delta_z**2)
        if delta_z != 0:
            theta3 = np.arctan(d3_plane / delta_z)
            F3 = (F / d3) * np.sin(theta3) #component of the force on the plane
        else:
            F3 = F / d3
        if d3x != 0:
            alfa3 = np.arctan(d3y / d3x)  # angle of the distance vector
        else:
            alfa3 = np.pi / 2
        F3x = F3 * np.cos(alfa3)
        F3y = F3 * np.sin(alfa3)
        a3x = F3x / self.mass
        a3y = F3y / self.mass
        if self.x >= m3.x:  # checking the sign of the acceleration
            a3x = - a3x
        if self.y >= m3.y:
            a3y = -a3y

        #sum of all the accelerations
        self.ax = a1x + a2x + a3x
        self.ay = a1y + a2y + a3y


    def Euler_approx(self):
        self.vx += self.ax * step
        self.vy += self.ay * step
        self.x += self.vx *step
        self.y += self.vy * step


    def check_if_caught(self, m1:Magnet, m2:Magnet, m3:Magnet):
        d1x = np.absolute(self.x - m1.x)
        d1y = np.absolute(self.y - m1.y)
        d1_plane = np.sqrt((d1x) ** 2 + (d1y) ** 2)
        d1 = np.sqrt((d1x) ** 2 + (d1y) ** 2 + delta_z ** 2)

        d2x = np.absolute(self.x - m2.x)
        d2y = np.absolute(self.y - m2.y)
        d2_plane = np.sqrt((d2x) ** 2 + (d2y) ** 2)
        d2 = np.sqrt((d2x)**2 + (d2y)**2 + delta_z**2)

        d3x = np.absolute(self.x - m3.x)
        d3y = np.absolute(self.y - m3.y)
        d3_plane = np.sqrt((d3x) ** 2 + (d3y) ** 2)
        d3 = np.sqrt((d3x)**2 + (d3y)**2 + delta_z**2)

        if d1 < m1.magnet_radius:
            self.x = m1.x
            self.y = m1.y
            self.vx = 0
            self.vy = 0
            self.color = m1.color
            return True

        elif d2 < m2.magnet_radius:
            self.x = m2.x
            self.y = m2.y
            self.vx = 0
            self.vy = 0
            self.color = m2.color
            return True

        if d3 < m3.magnet_radius:
            self.x = m3.x
            self.y = m3.y
            self.vx = 0
            self.vy = 0
            self.color = m3.color
            return True

        return False



M1 = Magnet(0.6, -0.6, red)
M2 = Magnet(-0.6, -0.6, yellow)
M3 = Magnet(0, 0.404, blue)
B1 = Ball(-0.62, 0.32, mass = 1)


def repetitions(n):
    #screen.fill(black)
    # n is the number of horizontal steps
    width = info.current_w / 350  # converts the current_w in meters
    height = info.current_h / 350  # converts the current_h in meters
    horizontal_step = width / n  # this assumes that width is greater that height
    n_vertical_steps = round(height / horizontal_step)  # this is the number of squares in a column
    matrix = np.zeros((n_vertical_steps, n))

    for i in range(n_vertical_steps):
        for j in range(n):
            B1.x = j * horizontal_step - (width / 2)
            B1.y = (height / 2) - i * horizontal_step
            internal_time = 0
            landed = False
            while not landed:
                landed = B1.check_if_caught(M1, M2, M3)
                if landed == True:
                    break
                if internal_time >= 20:
                    matrix [i,j] = 4
                    B1.color = brown
                    landed = True
                screen.fill(white)
                B1.draw()
                pygame.display.update()
                B1.calculate_acceleration_squared(M1, M2, M3)
                B1.Euler_approx()
                internal_time += step


            if B1.x == M1.x and B1.y == M1.y:
                matrix[i,j] = 1

            elif B1.x == M2.x and B1.y == M2.y:
                matrix[i, j] = 2

            elif B1.x == M3.x and B1.y == M3.y:
                matrix[i, j] = 3

    for i in range(n_vertical_steps):
        for j in range(n):
            if matrix[i,j] == 1:
                x_square = (j * horizontal_step) - (width / 2)
                y_square = (height / 2) - (i * horizontal_step)
                x_square, y_square = unit_conversion(x_square), unit_conversion(y_square)
                side = unit_conversion(horizontal_step)
                pos = list(coordinate_converter(x_square, y_square))
                pos.append(side)
                pos.append(side)
                pygame.draw.rect(screen, M1.color, pos)
                #screen.set_at((round(x_square), round(y_square)), M1.color)
                pygame.display.update()
            elif matrix[i,j] == 2:
                x_square = (j * horizontal_step) - (width / 2)
                y_square = (height / 2) - (i * horizontal_step)
                x_square, y_square = unit_conversion(x_square), unit_conversion(y_square)
                side = unit_conversion(horizontal_step)
                pos = list(coordinate_converter(x_square, y_square))
                pos.append(side)
                pos.append(side)
                pygame.draw.rect(screen, M2.color, pos)
                #screen.set_at((round(x_square), round(y_square)), M2.color)
                pygame.display.update()
            elif matrix[i,j] == 3:
                x_square = (j * horizontal_step) - (width / 2)
                y_square = (height / 2) - (i * horizontal_step)
                x_square, y_square = unit_conversion(x_square), unit_conversion(y_square)
                side = unit_conversion(horizontal_step)
                pos = list(coordinate_converter(x_square, y_square))
                pos.append(side)
                pos.append(side)
                pygame.draw.rect(screen, M3.color, pos)
                #screen.set_at((round(x_square), round(y_square)), M3.color)
                pygame.display.update()

            elif matrix[i,j] == 4:
                x_square = (j * horizontal_step) - (width / 2)
                y_square = (height / 2) - (i * horizontal_step)
                x_square, y_square = unit_conversion(x_square), unit_conversion(y_square)
                side = unit_conversion(horizontal_step)
                pos = list(coordinate_converter(x_square, y_square))
                pos.append(side)
                pos.append(side)
                pygame.draw.rect(screen, brown, pos)
                #screen.set_at((round(x_square), round(y_square)), brown)
                pygame.display.update()
    #print(matrix)


repetitions(5)
running = True
while running:
    """screen.fill(red)
    caught = B1.check_if_caught(M1, M2, M3)
    if not caught:
        B1.calculate_acceleration(M1, M2, M3)
        B1.Euler_approx()
    B1.draw()
    M1.draw()
    M2.draw()
    M3.draw()"""
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


pygame.quit()
