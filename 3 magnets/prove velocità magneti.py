import time
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import threading
import ctypes as c

#This code uses the multiprocessing library, it does its task using all 4 CPU cores available on pc
#Threading wasn't used because it didn't really improve permformances: multiprocessing is better with CPU intense codes
#Furthermore, the simultaneity with threads is just an illusion: the threads are executed by the cpu one after the other


step = 0.001
F = 10 #absolute magnetic force
delta_z = 0 #distance of the plane of the moving mass from the magnets



def unit_conversion(n):
    #takes in input a number in meters and converts it in pixels
    #350 is the factor of conversion, so 1m = 350 pixels
    n *= 350
    return n

class Magnet:
    def __init__(self, x, y ,force = F):
        self.x = x
        self.y = y
        self.F = F
        self.magnet_radius = 0.06 # meters


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
            return True

        elif d2 < m2.magnet_radius:
            self.x = m2.x
            self.y = m2.y
            self.vx = 0
            self.vy = 0
            return True

        if d3 < m3.magnet_radius:
            self.x = m3.x
            self.y = m3.y
            self.vx = 0
            self.vy = 0
            return True

        return False

#creating the 3 magnets
M1 = Magnet(0.6, -0.6)
M2 = Magnet(-0.6, -0.6)
M3 = Magnet(0, 0.44)

#defining the bounds of the interval that will be displayed using matplotlib
x_lower_bound = -2
x_upper_bound = 2
y_lower_bound = -2
y_upper_bound = 2


rows, columns = 10,10 #this is the resolution of the simulation

jump = abs(x_upper_bound - x_lower_bound) / rows #the step between a point to test and the next


def run_simulation(row_start, row_end, matrix, id):
    #this function is passed to the 4 process objects that run the simulation
    #it calculates on which magnet the ball falls and sets in the corresponding place in the matrix representing the space
    #the number of the magnet
    #it also prints at what percentage of the work the process is on
    #it takes in input the starting row, the ending row (the work is split in 4), the matrix representing the plane and the id
    #the id is just a number to identify the process
    counter = 0 + row_start * columns
    B = Ball(0,0, mass = 1)
    n_repetitions = (row_end - row_start) * columns
    percentage = 0
    for i in range(row_end - row_start):
        for j in range(columns):
            #in this loop there is the simulation
            B.x = j * jump - abs(x_upper_bound - x_lower_bound) / 2
            B.y = y_upper_bound - i * jump - row_start * jump #with these 2 steps the ball is placed in the correct starting position
            internal_time = 0
            landed = False
            while not landed:
                landed = B.check_if_caught(M1, M2, M3)
                if landed == True:
                    break
                if internal_time >= 60:
                    matrix[counter] = 4
                    landed = True
                    
                B.calculate_acceleration(M1, M2, M3)
                B.Euler_approx()
                internal_time += step

            if B.x == M1.x and B.y == M1.y:
                matrix[counter] = 1
                

            elif B.x == M2.x and B.y == M2.y:
                matrix[counter] = 2
               

            elif B.x == M3.x and B.y == M3.y:
                matrix[counter] = 3
            counter += 1
            percentage += 1
            print(f"{id})  ",percentage / n_repetitions * 100, " %")


def run_one_simulation(row_start, row_end, matrix):
    #this function is used in case you don't want to split the work in 4, it's practically identical to the one above
    counter = 0 + row_start * columns
    B = Ball(0,0, mass = 1)
    for i in range(row_end - row_start):
        for j in range(columns):
            B.x = j * jump - abs(x_upper_bound - x_lower_bound) / 2
            B.y = y_upper_bound - i * jump - row_start * jump
            internal_time = 0
            landed = False
            while not landed:
                landed = B.check_if_caught(M1, M2, M3)
                if landed == True:
                    break
                if internal_time >= 60:
                    matrix[counter] = 4
                    landed = True
                    
                B.calculate_acceleration(M1, M2, M3)
                B.Euler_approx()
                internal_time += step

            if B.x == M1.x and B.y == M1.y:
                matrix[counter] = 1
                

            elif B.x == M2.x and B.y == M2.y:
                matrix[counter] = 2
               

            elif B.x == M3.x and B.y == M3.y:
                matrix[counter] = 3
            counter += 1
    return matrix


def main():
    #this is the main
    mp_arr = mp.Array(c.c_double, rows*columns)
    a = mp.Process(target = run_simulation, args = (0,round(rows/4), mp_arr, 1))
    b = mp.Process(target = run_simulation, args = (round(rows/4), round(rows/2), mp_arr,2))
    cv = mp.Process(target = run_simulation, args = (round(rows/2),round(rows/4*3), mp_arr,3))
    d = mp.Process(target = run_simulation, args = (round(rows/4*3), rows, mp_arr,4))
    #here the 4 Process objects are created and to each one is assigned 1/4 of the total work to do

    a.start()
    b.start()
    cv.start()
    d.start()
    
    a.join()
    b.join()
    cv.join()
    d.join()#the join function is used to wait that all processes are finished
    
    arr = np.frombuffer(mp_arr.get_obj()) #this is used to recover data from the shared matrix, but it's in 1 dimension
    b = arr.reshape((rows, columns))#this reshapes the array in the correct 2 dimension format

    
    """b = np.zeros((rows,columns)).ravel()
    b = run_one_simulation(0,rows, b)
    b = b.reshape((rows,columns))""" #uncomment this if you don't want to split work
    print("runtime: ", time.perf_counter(), "  seconds") #prints the runtime at the end

    plt.title('3 fixed body system')
    plt.imshow(b, extent = [x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound])
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.show()


if __name__ == '__main__': #this statement is needed so that the other processes don't execute other commands and only the main is completely executed
    main()
