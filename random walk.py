import pygame
import numpy as np

pygame.init()
info = pygame.display.Info()
h = info.current_h
w = info.current_w
screen = pygame.display.set_mode((w,h), pygame.NOFRAME)
red = (230,50,50)
green = (0, 255, 0)
blue = (0, 0, 128)
brown = (127,64,0)
yellow = (255,255,0)
white = (255, 255, 255)
black = (0,0,0)
violet = (127,0,255)

step = 1
repetitions = 5000

class Point:
    def __init__(self, color ,x = 0, y = 0):
        self.color = color
        self.x = x
        self.y = y
    def change_color(self):
        a,b = coordinate_converter(self.x,self.y)
        pygame.draw.rect(screen, self.color, (a,b, step, step))
        
        
        
def coordinate_converter(x,y):
    a,b = x + int(info.current_w/2), int(info.current_h/2) - y
    return a,b

P = Point(white)

def walk(a:Point,s):
    """ generates the random walk given a step and a point"""
    n = np.random.randint(1,9)
    if n == 1:
        a.x -=s
        a.y += s
        
    elif n == 2:
        a.x -=0
        a.y += s

    elif n == 3:
        a.x += s
        a.y += s

    elif n == 4:
        a.x += s
        a.y -= 0

    elif n == 5:
        a.x += s
        a.y -= s

    elif n == 6:
        a.x -= 0
        a.y -= s

    elif n == 7:
        a.x -= s
        a.y -= s

    elif n == 8:
        a.x -= s
        a.y += 0
        
    a.change_color()
    
running = True
screen.fill(black)
run_finished = False
while running:
    if not run_finished:
        screen.fill(black)
        P.x = 0
        P.y = 0
        for i in range(repetitions):
            walk(P,step)
            run_finished = True
            pygame.display.update()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run_finished = True
            running = False
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            run_finished = False
pygame.quit()