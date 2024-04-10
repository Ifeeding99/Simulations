#this program permits to see sensitive dependence on initial condition for the logistic equation
import matplotlib.pyplot as plt

R = 2.9 #growth rate
iterations = 100

x1 = 0.3 #real value
x2 = 0.3001 #eximated value (has some errors)
err = abs(x1 - x2) #error between the 2 numbers

list1 = []
list2 = []
time = []
errors = []

logistic_equation = lambda x: R*x*(1-x) #the function, it's simply the logistic equation (yes, I wanted to use lambdas)

for i in range(iterations): #iteration cycle
    time.append(i)
    list1.append(x1)
    list2.append(x2)
    errors.append(err)
    x1 = logistic_equation(x1)
    x2 = logistic_equation(x2)
    err = abs((x1 - x2))

#displaying results
fig, ax = plt.subplots(1,2)

#the first graph is the orbit of the real value against the orbit of the eximated value
ax[0].plot(time,list1, color = 'blue', label = 'x1', marker = '.')
ax[0].plot(time,list2, color = 'red', label = 'x2', marker = '.')
ax[0].grid()
ax[0].legend(loc='best')
ax[0].set_ylim(0,1)
ax[0].set_xlabel('iterations')
ax[0].set_ylabel('population')

#the second graph is the value of the error iteration by iteration
ax[1].plot(time,errors, color = 'red', label = 'error', marker = '.')
ax[1].grid()
ax[1].legend(loc='best')
ax[1].set_xlabel('iterations')
ax[1].set_ylabel('error')

plt.show()

'''
OBSERVATIONS:
It seems that when there is a fixed point attractor the error decreases exponentially.
When you are in the chaotic regime instead, the error grows exponentially, reaches a maximum and then fluctuates randomly.
The last concept it's a confirmation of the butterfly effect.

INTERESTING OBSERVATIONS FOR R = 3.838:
If you choose x1 as 2.0 and x2 as 2.001 first the error grows but then it suddenly decays and becomes almost 0;
but paradoxically, if x2 is 2.0001, after a rapid ramping up, the error fluctuates periodically between approximately 0.8 and 0.2.
The same is true for x2 = 2.01, moreover the values between the error oscillates in this case are the same as the ones before (0.8 and 0.2).
In these cases the graphs of the populations appears to be out of phase, but for x2 = 2.001 the graphs are in phase.
I don't have a clear idea of why a more accurate measurement has a greater error than a lesser accurate one in the long run, it seems paradoxical.
I currently don't know what it takes for the orbits to get in phase and make the error shrink, it could be that this is a chaotic process.

OBSERVATIONS FOR 3<R<(3+sqrt(6)):
For these values of R the attractor is a cycle of 2 points.
If the initial error is greater than 0.1 the graphs appear to be out of phase and the error increases until it assumes a critical value and remains constant.
This could be explained by the fact that different initial conditions reach the attractor at different times.
But if the initial error is less than 0.002 it decays exponentially, so if the initial conditions are less than 0.09 apart they will be in phase.
By increasing R the time for getting them in phase increases as the error does in the case that the initial conditions differ for more than 0.09.
This is not true for values between 0.3 and 0.4, where even an error lesser than 0.5 or 0.2 will be magnified (dunno why, probably has to do with the value of the firt iterations, that was the explanation for x1+x2=1 case).

OBSERVATIONS FOR (3+sqrt(6))<R<3.54409:
For these values of R the attractor is a cycle of 4 points.
With these conditions, if the initial error is lesser than 0.01 it shrinks and the graphs are in phase.
However if that is not the case, the error ramps up and oscillates periodically (so the orbits are out of phase).
BUT there are special cases: for example if x1 = 0.2 and x2 = 0.8 the error decays almost immediately after only 1 iteration (dunno why).
EVEN IN THE CHAOTIC REGIME (R = 4) THEIR ORBITS WILL BE THE SAME FOR ALMOST 40 ITERATIONS!! WTF
For values that results in fixed attractor the error between the orbits will get to 0 after 1 iteration.
EDIT: I figured out why:
That will be discussed in the next paragraph

OBSERVATIONS FOR X1 + X2 = 1:
If x1+x2=1 we can write x2 as (1-x1) and x1 as (1-x2).
The first value of the itinerary for x1 will be equal to R*x1*(1-x1), but (1-x1) is equal to x2, so we can write 
that the first iteration for x1 will be R*x1*x2.
For x2 it's the same.
The first value of the orbit of x2 will be R*x2*(1-x2), but (1-x2) is equal to x1, so we can write
that the first iteration for x2 will be R*x1*x2 too.
The first iteration gives exactly the same number for any x1, x2 such that x1+x2 = 1.
I think my computer makes the values diverge after 40 iterations in the chaotic regime because of the approximations it makes.
This could represent another proof for the butterfly effect: the error made by the computer grows exponentially.
Now, this consideration is important: this phenomenon tells us that very different staring conditions can follow very similar orbits, if not even equal ones.
And you can demonstrate the existence of such values algebraically! (makes me think of Smale's Horseshoe: nearby points get far apart while distant points get closer)
'''