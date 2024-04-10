import numpy as np
import matplotlib.pyplot as plt

n_leaves = 0
leaves_per_turn = 1000
leaves_turn = 3
rabbits_pop = 150
foxes_pop = 10
loss_per_turn = 10

class Rabbit:
    def __init__(self,energy,alive):
        self.energy = energy
        self.alive = alive
        self.leaves_per_rabbit = 8
        self.energy_per_leaf = 3
        self.energy_to_reproduce = 10
    def eat(self,n_l,r_p):
        p = n_l/(self.leaves_per_rabbit*r_p)
        for i in range(self.leaves_per_rabbit):
            n = np.random.random()
            if n <= p:
                n_l -= 1
                self.energy += self.energy_per_leaf
        return n_l


class Fox:
    def __init__(self,energy,alive):
        self.energy = energy
        self.alive = alive
        self.rabbits_per_fox = 15
        self.energy_per_rabbit = 5
        self.energy_to_reproduce = 15
    def eat(self,r_p,f_p):
        p = r_p/(self.rabbits_per_fox*f_p)
        for i in range(self.rabbits_per_fox):
            n = np.random.random()
            if n <= p:
                r_p -= 1
                self.energy += self.energy_per_rabbit
        return r_p


rabbits_list = [Rabbit(7,True) for i in range (rabbits_pop)]
foxes_list = [Fox(7,True) for i in range (foxes_pop)]
time = []
rabbits = []
foxes = []
leaves = []

for i in range(10000):
    time.append(i)
    rabbits.append(len(rabbits_list))
    foxes.append(len(foxes_list))
    leaves.append(n_leaves)

    if i % leaves_turn == 0:
        n_leaves += leaves_per_turn

    r_pop = len(rabbits_list)
    f_pop = len(foxes_list)

    for r in rabbits_list:
        n_leaves = r.eat(n_leaves,r_pop)

    for f in foxes_list:
        r_pop = f.eat(r_pop,f_pop)


    killed_rabbits = len(rabbits_list) - r_pop
    for bb in range(killed_rabbits):
        cc = len(rabbits_list)
        k_r = np.random.randint(0,cc)
        rabbits_list.pop(k_r)


    l_r = len(rabbits_list)
    l_f = len(foxes_list)
    for a in range(l_r):
        rabbits_list[a].energy -= loss_per_turn
        if rabbits_list[a].energy <= 0:
            rabbits_list[a].alive = False
        elif rabbits_list[a].energy >= rabbits_list[a].energy_to_reproduce:
            for b in range(3):
                rabbits_list.append(Rabbit(7,True))
    rabbits_list = [r for r in rabbits_list if r.energy > 0 and r.alive == True]


    for a in range(l_f):
        foxes_list[a].energy -= loss_per_turn
        if foxes_list[a].energy <= 0:
            foxes_list[a].alive = False
        if foxes_list[a].energy >= foxes_list[a].energy_to_reproduce:
            for b in range(2):
                foxes_list.append(Fox(7,True))
    foxes_list = [f for f in foxes_list if f.energy > 0 and f.alive == True]

fig, ax = plt.subplots(1,2)
ax[0].plot(time,leaves, color = 'green',label = 'leaves')
ax[0].plot(time,rabbits, color = 'yellow', label = 'rabbits')
ax[0].plot(time,foxes, color = 'red', label = 'foxes')
ax[0].legend(loc = 'best')
ax[0].grid()
ax[1].plot(rabbits,foxes, marker = '.', linestyle = '', markersize = 1)
ax[1].grid()
plt.show()


