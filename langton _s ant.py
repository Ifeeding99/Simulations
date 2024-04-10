w'''
THE RULES:
The entire screen is viewed as a grid of squares,
- Initially the ant is positioned in the center
- If it stands on a white square,it will turn 90° clockwise, flip the color of the square and move forward by one unit
- If it stands on a black square it will turn 90° counterclockwise, flip the color of the square and move forward by one unit

Because of I use a black background, I programmed the ant to turn clockwise on black squares and counterclockwise on white squares.
The result is the same
'''

import pygame

step = 4 #set at 1 to color only single pixels

pygame.init()
red = (230, 50, 50)
green = (0, 255, 0)
blue = (0, 0, 128)
brown = (127, 64, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
violet = (127, 0, 255)
info = pygame.display.Info()

screen = pygame.display.set_mode((int(info.current_w), int(info.current_h)), pygame.NOFRAME)


def coordinate_converter(x, y):
    b = x + int(info.current_w / 2), int(info.current_h / 2) - y
    return b


class Ant:
    def __init__(self, color, orientation='W'):
        self.color = color
        self.orientation = orientation
        self.pos_x = 0
        self.pos_y = 0

    def change_orientation(self):
        c = screen.get_at(coordinate_converter(self.pos_x, self.pos_y))
        if c == black:
            if self.orientation == 'E':
                self.orientation = 'S'


            elif self.orientation == 'S':
                self.orientation = 'W'

            elif self.orientation == 'W':
                self.orientation = 'N'

            elif self.orientation == 'N':
                self.orientation = 'E'
        else:
            if self.orientation == 'E':
                self.orientation = 'N'

            elif self.orientation == 'S':
                self.orientation = 'E'

            elif self.orientation == 'W':
                self.orientation = 'S'

            elif self.orientation == 'N':
                self.orientation = 'W'
    def move(self):
        c = screen.get_at(coordinate_converter(self.pos_x, self.pos_y))
        x,y = coordinate_converter(self.pos_x, self.pos_y)
        if c == black:
            pygame.draw.rect(screen, white, (x,y, step, step))
        elif c == white:
            pygame.draw.rect(screen, black, (x,y, step, step))

        if self.orientation == 'N':
            self.pos_y += step

        if self.orientation == 'E':
            self.pos_x += step

        if self.orientation == 'W':
            self.pos_x -= step

        if self.orientation == 'S':
            self.pos_y -= step

A = Ant(white)
running = True
screen.fill(black)

while running:
    A.move()
    A.change_orientation()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
