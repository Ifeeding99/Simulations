import pymunk
import pygame

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
pygame.display.set_caption("Double pendulum")
FPS = 100

clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -981 # put -981 if you want a more realistic simulation
ball_radius = 10

def converter_pymunk_to_pygame(pos):
    #takes in input body.position
    return round(pos[0]), round(h - pos[1])

class Ball:
    def __init__(self, x = 300, y = 350, mass = 10):
        self.body = pymunk.Body(mass)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        X,Y = converter_pymunk_to_pygame(self.body.position)
        pygame.draw.circle(screen, red, (X,Y), ball_radius)

class Attachment_point:
    def __init__(self, x, y):
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = x, y


class String:
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
        joint = pymunk.PinJoint(self.b1, self.b2)
        space.add(joint)

    def draw(self):
        x1, y1 = converter_pymunk_to_pygame(self.b1.position)
        x2, y2 = converter_pymunk_to_pygame(self.b2.position)
        pygame.draw.line(screen, white, (x1,y1), (x2,y2), 1)


# parameters
anchor_point = Attachment_point(w/2, h/2)
b1 = Ball(x = w/3, y = 300, mass = 10)
b2 = Ball(x = w/2 - 100, y = 500, mass = 10)
string1 = String(anchor_point.body, b1.body)
string2 = String(b1.body, b2.body)


running = True
while running:
    screen.fill(black)
    b1.draw()
    b2.draw()
    string1.draw()
    string2.draw()
    pygame.display.update()
    clock.tick(FPS)
    space.step(1/FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()