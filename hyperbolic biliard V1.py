#the best version of this code is the V2
#this was a prototype
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

box_side = 5
step = 0.001
a = 1  # x semi-axis
b = 0.5  # y semi-axis
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

    def reflected_on_straight_walls(self):
        if 2 > self.x > -2:
            self.vy = -self.vy  # the straight walls are on the northern and southern sides
        else:
            self.vx = -self.vx

    def reflected_on_hyperbola(self):
        # To get the coordinates of the points of collision I have to take the ball's x and y
        # and add the radius, it's as if the center of mass collides with a wall in front of the real one
        # and that is parallel to the latter
        # I calculate the tangent line via the derivative in that point and then the normal
        # using the derivative again
        # the equation of the hyperbola is (x/a)**2 - (y/b)**2 = 1
        # the derivative is dy/dx = (x/y)*(b/a)**2
        P = (self.x, self.y)  # point of collision
        if P[0] > 0:  # this is because the ball is not a point, so the center of mass will never hit the hyperbola
            # but it is as if it hits another hyperbola that is traslated towards the ball
            m_tangent = ((P[0] - self.radius) / P[1]) * (b / a) ** 2
        else:
            m_tangent = ((P[0] - self.radius) / P[1]) * (b / a) ** 2

        if m_tangent == 0:
            m_normal = 1000000
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
            self.vx -= 2 * projected_vector_x
            if m_normal > 0:
                self.vy -= 2 * projected_vector_y
            else:
                self.vy += 2 * projected_vector_y

        else:
            # controlling if the ball is in the second or third quadrant (in which self.vx is negative,
            # so projected_vector_x should be positive)
            self.vx += 2 * projected_vector_x
            if m_normal > 0:
                self.vy += 2 * projected_vector_y
            else:
                self.vy -= 2 * projected_vector_y


B1 = Ball(0, 0, 25, -19)

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid()

c = np.sqrt(a ** 2 + b ** 2)  # calculates the focal distance of the hyperbola
reflection_hyperbola_a = np.sqrt((c - B1.radius) ** 2 - b ** 2)  # because the ball has a radius it is as
# if the center of mass hits a narrower hyperbola


# here I have just calculated the a parameter of the new hyperbola
# here's the math:
# c = sqrt(a**2 + b**2), a is the intercept with x axis, c is the focal distance
# the new hyperbola has a narrower focal distance that is c - r where r is the radius of the ball
# so we have (c - r) = sqrt(a**2 + b**2)
# solving for a we obtain a = sqrt((c - r)**2 - b**2)
# and that's our new parameter
def animate(i):
    B1.update_coordinates()
    d = (B1.x / reflection_hyperbola_a) ** 2 - (B1.y / b) ** 2
    if d >= 1:
        # the hyperbola is defined as the locus of points whose difference of the distance between the 2 foci is costant
        # so if the difference is smaller than 1 a point is "inside" the space delimited by the hyperbola
        # if the distance is exactly 1 the point is on the hyperbola
        # if the distance is greater than 1 the point is beyond the hyperbola
        B1.reflected_on_hyperbola()
    elif B1.y >= (box_side/2 - B1.radius) or B1.y <= (-box_side/2 + B1.radius):
        B1.reflected_on_straight_walls()

    elif B1.x >= (box_side/2 - B1.radius) or B1.x <= (-box_side/2 + B1.radius):
        B1.reflected_on_straight_walls()
    ball = plt.Circle((B1.x, B1.y), radius=B1.radius)
    ax.add_artist(ball)
    ax.contour(x, y, z, [1])


ani = FuncAnimation(fig, animate, interval=10)
plt.show()
