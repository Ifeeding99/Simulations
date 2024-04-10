# This is the definitive code for reflection on a hyperbola

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

box_side = 4
step = 0.001  # if the simulation is imprecise just decrease the stepsize,
# if the ball is going really fast (like 100 m/s) you should do it

a = 1  # x semi-axis
b = 1  # y semi-axis
c = np.sqrt(a ** 2 + b ** 2)
f1 = (-c, 0)
f2 = (c, 0)
x = np.linspace(-(box_side / 2), (box_side / 2), 1000)
y = np.linspace(-(box_side / 2), (box_side / 2), 1000)
x, y = np.meshgrid(x, y)
z = (x / a) ** 2 - (y / b) ** 2


class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 0.07  # radius of the ball

    def update_coordinates(self):
        self.x += self.vx * step
        self.y += self.vy * step

    def reflected_on_hyperbola(self):
        # To get the coordinates of the points of collision I have to take the ball's x and y
        # and add the radius, it's as if the center of mass collides with a wall in front of the real one
        # and that is parallel to the latter
        # I calculate the tangent line via the derivative in that point and then the normal
        # using the derivative again
        # the equation of the hyperbola is (x/a)**2 - (y/b)**2 = 1
        # the derivative is dy/dx = (x/y)*(b/a)**2
        P = (self.x, self.y)  # point of collision

        # this if statement checks if the point of collision is the vertex of the hyperbola
        if P[1] == 0:
            m_tangent = 1000000000
        else:
            if P[0] > 0:  # this is because the ball is not a point, so the center of mass will never hit the hyperbola
                # but it is as if it hits another hyperbola that is traslated towards the ball
                m_tangent = ((P[0] - self.radius) / P[1]) * (b / a) ** 2
            else:
                m_tangent = ((P[0] - self.radius) / P[1]) * (b / a) ** 2

        if m_tangent == 0:
            m_normal = 1000000000
        else:
            m_normal = -(1 / m_tangent)
        angle_normal = np.arctan(abs(m_normal))  # angle between x axis and normal
        module_velocity = np.sqrt(self.vx ** 2 + self.vy ** 2)
        if self.vx == 0:
            m_velocity = 1000000
        else:
            m_velocity = (self.vy / self.vx)  # m of velocity vector
        if m_velocity * m_normal == -1:
            angles_between_lines = np.pi / 2

        else:
            angles_between_lines = np.arctan(abs((m_velocity - m_normal) / (
                    1 + m_velocity * m_normal)))  # formula for calculating the angle between 2 lines
        # the formula is tan(a)=|(m1-m2)/(1+m1*m2)|
        module_projected_vector = abs(module_velocity * np.cos(angles_between_lines))
        projected_vector_x = abs(module_projected_vector * np.cos(angle_normal))
        projected_vector_y = abs(module_projected_vector * np.sin(angle_normal))

        # now I have to establish the sign of the projected vector components
        # projected_vector_x always has a sign opposite to the one of self.vx
        # if the m of the normal to the tangent is positive, then projected_vector_y will be positive
        # else it will be negative

        if P[0] > 0:
            # controlling if the ball is in the first or fourth quadrant (in which self.vx is positive,
            # so projected_vector_x should be negative)
            if self.vx > 0:
                self.vx -= 2 * projected_vector_x
                if m_normal > 0:
                    self.vy -= 2 * projected_vector_y
                else:
                    self.vy += 2 * projected_vector_y

        else:
            # controlling if the ball is in the second or third quadrant (in which self.vx is negative,
            # so projected_vector_x should be positive)
            if self.vx < 0:
                self.vx += 2 * projected_vector_x
                if m_normal > 0:
                    self.vy += 2 * projected_vector_y
                else:
                    self.vy -= 2 * projected_vector_y


B1 = Ball(0, 0, 25, 4)


X_list = []  # list of x coordinates that the ball assumes
Y_list = []  # list of y coordinates that the ball assumes
iterations = 6000
x_hyperbola_1 = np.linspace(-box_side / 2, -a, 1000)
x_hyperbola_2 = np.linspace(a, box_side / 2, 1000)
y_hyperbola_1 = []
y_hyperbola_2 = []

for j in range(1000):
    y1 = np.sqrt((x_hyperbola_1[j] ** 2 / a ** 2 - 1) * b ** 2)
    y2 = -np.sqrt((x_hyperbola_1[j] ** 2 / a ** 2 - 1) * b ** 2)
    y_hyperbola_1.append([y1, y2])

for k in range(1000):
    y1 = np.sqrt((x_hyperbola_2[k] ** 2 / a ** 2 - 1) * b ** 2)
    y2 = -np.sqrt((x_hyperbola_2[k] ** 2 / a ** 2 - 1) * b ** 2)
    y_hyperbola_2.append([y1, y2])

last_collision = 0  # 2 collisions can't happen at a distance of only 1 step
for i in range(iterations):
    X_list.append(B1.x)
    Y_list.append(B1.y)
    B1.update_coordinates()

    d1 = ((B1.x - B1.radius) / a) ** 2 - (B1.y / b) ** 2
    d2 = ((B1.x + B1.radius) / a) ** 2 - (B1.y / b) ** 2

    # this if statement checks if the ball collides with the point where the hyperbola intersects the wall
    if (d1 >= 1 or d2 >= 1) and 2 - abs(B1.x) <= B1.radius:
        if i > (last_collision + 1):
            last_collision = i
            B1.vx = -B1.vx
            B1.vy = -B1.vy

    elif d1 >= 1 or d2 >= 1:
        # the hyperbola is defined as the locus of points whose difference of the distance between the 2 foci is costant
        # so if the difference is smaller than 1 a point is "inside" the space delimited by the hyperbola
        # if the distance is exactly 1 the point is on the hyperbola
        # if the distance is greater than 1 the point is beyond the hyperbola
        if i > (last_collision + 1):
            last_collision = i
            B1.reflected_on_hyperbola()

    # this if statement checks if the ball collides with the corner
    if 2 - abs(B1.x) <= B1.radius and 2 - abs(B1.y) <= B1.radius:
        if i > (last_collision + 1):
            last_collision = i
            B1.vx = -B1.vx
            B1.vy = -B1.vy

    # this checks if the ball collides with the top or bottom wall
    elif B1.y >= (box_side / 2 - B1.radius) or B1.y <= (-box_side / 2 + B1.radius):
        if i > (last_collision + 1):
            last_collision = i
            B1.vy = -B1.vy

    # this checks if the ball collides with the right or left wall
    elif B1.x >= (box_side / 2 - B1.radius) or B1.x <= (-box_side / 2 + B1.radius):
        if i > (last_collision + 1):
            last_collision = i
            B1.vx = -B1.vx

fig, ax = plt.subplots()


def animate(i):
    plt.cla()
    ax.grid()
    ax.plot(x_hyperbola_1, y_hyperbola_1, color='blue')
    ax.plot(x_hyperbola_2, y_hyperbola_2, color='blue')
    ball = plt.Circle((X_list[i], Y_list[i]), radius=B1.radius)
    ax.add_artist(ball)
    ax.set_aspect('equal')
    ax.set_xlim(-box_side / 2, box_side / 2)
    ax.set_ylim(-box_side / 2, box_side / 2)
    ax.text(2.1, -2, f'iteration: {i}')


ani = FuncAnimation(fig, animate, frames=iterations, interval=50)
plt.show()
