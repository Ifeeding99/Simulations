import pygame
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import turtle

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
pygame.display.set_caption("Travelling salesman problem")


def from_screen_to_cartesian(x_screen,y_screen):
    #converts pygame coordinates in cartesian ones
    x_cart = x_screen - w/2
    y = h - y_screen
    y_cart = y - h/2
    return x_cart, y_cart

def from_cartesian_to_screen(x,y):
    #converts cartesian coordinates in the corresponding ones on the pygame screen
    x_screen = x + w/2
    y_screen = h/2 - y
    return x_screen, y_screen


class Point:
    def __init__(self, x, y ):
        self.x = x
        self.y = y

class Y_N_box:
    def __init__(self, y):
        self.y = y #'y' if it's yes 'n' if it's no
        if self.y == 'y':
            self.color = green
        else:
            self.color = red
    def change_color(self):
        if self.color == yellow and self.y == 'y':
            self.color = green
        elif self.color == yellow and self.y == 'n':
            self.color = red
        else:
            self.color = yellow
    def draw(self,x,y,s):
        self.text_rect = pygame.draw.rect(screen, self.color, (x,y,s,s))


points_list = {}

def choice_of_start_point():
    start_point = Point(0,0)
    s = 20
    screen.fill(black)
    font = pygame.font.Font('freesansbold.ttf', 16)
    phrase = "Do you want to choose the starting point with your mouse?"
    y = Y_N_box('y')
    n = Y_N_box('n')
    text = font.render(phrase, True, white, black)
    rect = text.get_rect()
    rect.center = (int(w/2),int(h/8))
    running = True
    while running:
        mpos = pygame.mouse.get_pos()
        screen.blit(text,rect)
        y.draw(int(w/2 - 3* s),int(h/8 + 20),s)
        n.draw(int(w/2 + 3* s),int(h/8 + 20),s)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and y.text_rect.collidepoint(mpos) and n.color != yellow:
                y.change_color()
                y.draw(int(w / 2 - 3 * s), int(h / 8 + 20), s)
                pygame.display.update()
                time.sleep(1)
                running1 = True
                running2 = False
                phrase = "Choose the starting point"
                text = font.render(phrase, True, white, black)
                rect = text.get_rect()
                rect.center = (int(w / 2), int(h / 8))
                screen.fill(black)
                while running1:
                    mpos = pygame.mouse.get_pos()
                    screen.blit(text, rect)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running1 = False
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running1 = False
                                pygame.quit()
                                sys.exit()

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.draw.circle(screen, green, (mpos[0], mpos[1]), 2)
                            pygame.display.update()
                            x_cor, y_cor = from_screen_to_cartesian(mpos[0], mpos[1])
                            start_point = Point(x_cor, y_cor)
                            time.sleep(1)
                            running = False
                            running1 = False

            elif event.type == pygame.MOUSEBUTTONDOWN and n.text_rect.collidepoint(mpos) and y.color != yellow:
                n.change_color()
                n.draw(int(w / 2 + 3 * s), int(h / 8 + 20), s)
                pygame.display.update()
                time.sleep(1)
                running2 = True
                running1 = False
                start_point.x = float(turtle.textinput("x coordinate", "Enter the x coordinate of the starting point"))
                start_point.y = float(turtle.textinput("y coordinate", "Enter the y coordinate of the starting point"))
                turtle.bye()
                turtle.Turtle._screen = None  # force recreation of singleton Screen object
                turtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
                screen.fill(black)
                while running2:
                    pygame.draw.circle(screen, green, (from_cartesian_to_screen(start_point.x, start_point.y)),2)
                    pygame.display.update()
                    time.sleep(1)
                    running2 = False
                    running = False

    return start_point


def choice_of_points_menu():
    s = 20
    n_choices = 0
    screen.fill(black)
    font = pygame.font.Font('freesansbold.ttf', 16)
    phrase = "Do you want to choose the points with your mouse?"
    text = font.render(phrase, True, white, black)
    rect = text.get_rect()
    rect.center = (int(w/2),int(h/8))
    y = Y_N_box('y')
    n = Y_N_box('n')
    running = True
    while running:
        mpos = pygame.mouse.get_pos()
        screen.blit(text,rect)
        st_x, st_y = from_cartesian_to_screen(start_point.x, start_point.y)
        pygame.draw.circle(screen, green, (st_x, st_y), 2)
        y.draw(int(w/2 - 3* s),int(h/8 + 20),s)
        n.draw(int(w/2 + 3* s),int(h/8 + 20),s)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()


            elif event.type == pygame.MOUSEBUTTONDOWN and y.text_rect.collidepoint(mpos) and n.color != yellow:
                y.change_color()
                y.draw(int(w / 2 - 3 * s), int(h / 8 + 20), s)
                pygame.display.update()
                time.sleep(1)
                running1 = True
                running2 = False
                phrase = "choose the points (press space bar to confirm)"
                text = font.render(phrase, True, white, black)
                rect = text.get_rect()
                rect.center = (int(w / 2), int(h / 8))
                screen.fill(black)
                while running1:
                    pygame.draw.circle(screen, green, (from_cartesian_to_screen(start_point.x, start_point.y)),2)
                    screen.blit(text, rect)
                    pygame.display.update()
                    mpos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running1 = False
                            running = False
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running1 = False
                                running = False
                                pygame.quit()
                                sys.exit()
                            elif event.key == pygame.K_SPACE:
                                running = False
                                running1 = False

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.draw.circle(screen, red, (mpos[0], mpos[1]), 2)
                            pygame.display.update()
                            x_cor, y_cor = from_screen_to_cartesian(mpos[0], mpos[1])
                            points_list[n_choices] = Point(x_cor, y_cor)
                            n_choices += 1

            elif event.type == pygame.MOUSEBUTTONDOWN and n.text_rect.collidepoint(mpos) and y.color != yellow:
                n.change_color()
                n.draw(int(w / 2 + 3 * s), int(h / 8 + 20), s)
                pygame.display.update()
                time.sleep(1)
                running1 = False
                running2 = True
                n_choices = int(turtle.textinput("number of points", "Enter the number of points you want to use"))
                for i in range (n_choices):
                    x = float(turtle.textinput("x coordinate", f"insert the x coordinate of the point number {i+1}"))
                    y = float(turtle.textinput("y coordinate", f"insert the y coordinate of the point number {i + 1}"))
                    points_list[i] = Point(x, y)

                turtle.bye()
                turtle.Turtle._screen = None  # force recreation of singleton Screen object
                turtle.TurtleScreen._RUNNING = True  # only set upon TurtleScreen() definition
                screen.fill(black)
                while running2:
                    pygame.draw.circle(screen, green, (from_cartesian_to_screen(start_point.x, start_point.y)),2)
                    for i in range (n_choices):
                        pygame.draw.circle(screen, red,
                                (from_cartesian_to_screen(points_list[i].x, points_list[i].y)),2)
                    pygame.display.update()
                    time.sleep(1)
                    running2 = False
                    running = False


    return n_choices

start_point = choice_of_start_point()
n_points = choice_of_points_menu()


population = 10
individuals_list = []
list_of_max = []
list_of_min = []
list_of_average = []


class Individual:
    def __init__(self, l):
        self.l = l
        self.D = 0
        self.perc = 0
        for i in range(len(self.l)-1):
            if i == 0:
                self.D += np.sqrt((start_point.x - points_list[self.l[i]].x)**2+
                                  (start_point.y - points_list[self.l[i]].y)**2)
            elif i == len(self.l)-2:
                self.D += np.sqrt((start_point.x - points_list[self.l[i+1]].x)**2+
                                  (start_point.y - points_list[self.l[i+1]].y)**2)

            else:
                self.D += np.sqrt((points_list[self.l[i]].x-points_list[self.l[i+1]].x)**2+
                                 (points_list[self.l[i]].y-points_list[self.l[i+1]].y)**2)

    def update_D(self):
        self.D = 0
        for i in range(len(self.l)-1):
            if i == 0:
                self.D += np.sqrt((start_point.x - points_list[self.l[i]].x)**2+
                                  (start_point.y - points_list[self.l[i]].y)**2)
            elif i == len(self.l)-2:
                self.D += np.sqrt((start_point.x - points_list[self.l[i+1]].x)**2+
                                  (start_point.y - points_list[self.l[i+1]].y)**2)

            else:
                self.D += np.sqrt((points_list[self.l[i]].x-points_list[self.l[i+1]].x)**2+
                                 (points_list[self.l[i]].y-points_list[self.l[i+1]].y)**2)


def generate_gen0(n_points, pop, i_l):
    for j in range(pop):
        i_l.append (Individual(list(np.random.choice([i for i in range(0,n_points)], size = n_points, replace = False))))
    return i_l

individuals_list = generate_gen0(n_points, population, individuals_list)

def mutation(el):
    n_points_to_replace = round(n_points * el.perc / 100)
    del_n = []
    for i in range(n_points_to_replace):
        while True:
            a = np.random.randint(0,n_points)
            if el.l[a] != 'c':
                del_n.append(el.l[a])
                el.l[a] = 'c'
                break

    if len(del_n) > 0:
        for j in range(n_points):
            if el.l[j] == 'c':
                b = int(np.random.choice(del_n))
                el.l[j] = b
                del_n.remove(b)
            else:
                pass

    return el

def fitness(individuals_list):
    average = 0
    for i in range(population):
        average += individuals_list[i].D
        for j in range(population):
            if j == (population - 1):
                break
            elif (individuals_list[j].D) > (individuals_list[j + 1].D):

                a = individuals_list[j + 1]
                individuals_list[j + 1] = individuals_list[j]
                individuals_list[j] = a

    average /= population
    list_of_max.append(individuals_list[0].D)
    list_of_min.append(individuals_list[-1].D)
    list_of_average.append(average)

    for i in range(population):
        individuals_list[i].perc = i * (100 / population)
        individuals_list[i] = mutation(individuals_list[i])
    for el in individuals_list:
        el.update_D()

    return individuals_list

gen = []
generations = 1000
for i in range (generations):
    gen.append(i)
    individuals_list = fitness(individuals_list)



screen.fill(black)
best = individuals_list[0]
for i in range(n_points + 1):
    if i == 0:
        pygame.draw.line(screen, white, (from_cartesian_to_screen(start_point.x, start_point.y))
        ,(from_cartesian_to_screen(points_list[best.l[0]].x, points_list[best.l[0]].y)))

    elif i == n_points:
        pygame.draw.line(screen, white,
        (from_cartesian_to_screen(points_list[best.l[-1]].x, points_list[best.l[-1]].y))
        ,(from_cartesian_to_screen(start_point.x, start_point.y)))
        points_list[best.l[0]].x, points_list[best.l[0]].y

    elif i != 0 and i != n_points:
        pygame.draw.line(screen, white,
                         (from_cartesian_to_screen(points_list[best.l[i-1]].x, points_list[best.l[i-1]].y)),
                         (from_cartesian_to_screen(points_list[best.l[i]].x, points_list[best.l[i]].y)))

font = pygame.font.Font('freesansbold.ttf', 16)
phrase = "Press ESC key to terminate"
text = font.render(phrase, True, white, black)
rect = text.get_rect()
rect.center = (int(w/2),int(h/8))

pygame.draw.circle(screen, green, (from_cartesian_to_screen(start_point.x, start_point.y)), 2)
for i in range(n_points):
    pygame.draw.circle(screen, red,
                       (from_cartesian_to_screen(points_list[i].x, points_list[i].y)),2)

running = True
while running:
    screen.blit(text, rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

plt.plot(gen, list_of_max, marker = '.', label = "least distance", color = 'red', linestyle = ' ')
plt.plot(gen, list_of_min, marker = '.', label = "maximum distance", color = 'blue', linestyle = ' ')
plt.plot(gen, list_of_average, marker = '.', label = "average distance", color = 'brown', linestyle = ' ')
plt.legend(loc = 'upper left')
plt.title("Travelling salesman graph")
plt.show()

