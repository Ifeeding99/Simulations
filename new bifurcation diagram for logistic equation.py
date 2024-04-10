#this code plots the bifurcation diagram for the iterated function x(n+1) = R*x(n) * (1 - x(n))
#the algorithm is this:
#You specify the number of R values you want (hence the stepsize between them), the number of iterations to ignore and the one to plot
#the logistic function is computed first as many times as the number of iterations to skip says, then the values x assumes are stored and plotted
import matplotlib.pyplot as plt
import numpy as np
import math

n_R = 1000 #this are the number of R tried, increase this to increase resolution
r_upper_bound = 4 #for the cubic set (the other one) set this to 7 or around that to see something
r_lower_bound = 0 #for the one with sine set it to the opposite of the upper bound to see the pattern
r_step = (r_upper_bound - r_lower_bound) / n_R
Rs = [r_lower_bound + i*r_step for i in range (n_R)] #array of all values of R


def graph(l):
    skip_iter = 300 #number of iterations to ignore
    plot_iter = 300 #number of points plotted
    results = []
    for n in l:
        x = np.random.random() #always picking a random seed between 0 and 1
        for i in range(skip_iter):
            x = n * x * (1 - x)
            #x = n * x ** 2 * (1 - x) #other version
            #x = n * np.sin ((np.pi * x) / 2) #version with sin(x)
            if x >= 100 or x <= -100:
                break
        fixed_points = []
        for j in range(plot_iter):
            if x < 100 and x > -100:
                x = n * x * (1 - x)
                #x = n * x ** 2 * (1 - x)
                #x = n * np.sin ((np.pi * x) / 2) #version with sin(x)
            else:
                break
            fixed_points.append(x) #takes all points between x fluctuate

        if (len(fixed_points)) == 0: #I needed this to fix an error: matplotlib can't plot if all elements of the array are not of the same size
            for v in range(plot_iter):
                fixed_points.append(x)
        fixed_points.sort()
        results.append(fixed_points)
    plt.plot(Rs,results,color='blue',marker=',',markersize=1,linestyle='',linewidth=0.1) #this is te main dish, change the parameters to get different views
    #for example removing the lines gives a total different picture
    plt.ylim(0,1) #for the iterated equation with sine the best is (-4,4), for the logistic equation the best is (0,1), same for the cubic one (the other one)
graph(Rs)
plt.show()

