import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
#this code simulates population growth using some parameters
#there are a finite number of nutrients, a fixed number of them is generated every iteration
#animals feed on these nutrients, energy is required to reeach the nutrient
#if the nutrient is near the animal will go for it else it won't
#if abother animal is near the same nutrient another one wants to eat a fight can start
#animals have an aggressivity associated with them, the higher the aggressivity the higher the possibility of a fight
#if the attacker's aggressivity is greater, the defender loses energy and the attacker conquers the chunk of food
#else the attacker loses energy


E_per_N = 40  #the amount of energy a single nutrient gives
number_of_nutrients = 200 #number of nutrients spawned for each iteration
number_of_animals = 200
energy_loss_per_step = 15 #energy used to stay alive
energy_to_reproduce = 20 #energy required to reproduce
energy_to_fight = 30 #energy wasted if the animal loses the fight
starting_energy = 20

class Nutrient:
    def __init__(self, x, y):
        self.x = x
        self.y = y

n_list = [Nutrient(np.random.randint(0,501),np.random.randint(0,501)) for i in range (number_of_nutrients)]
#this generates the nutrients at random locations

class Animal:
    def __init__(self, x, y, E, A):
        self.x = x
        self.y = y
        self.energy = E
        self.aggressivity = A
        self.alive = True
        self.stop_eating = 4 #number of nutrients eaten before feeling sated

    def catch(self, a_list): #function used by the animal to feed itself
        eaten_count = 0
        n_fights = 0
        global n_list
        for n in n_list: #iterates over all cunk of food and cheks which ones are at reach
            if eaten_count >= self.stop_eating: #checks if the animal is sated
                break
            d1 = np.sqrt((self.x - n.x)**2+(self.y - n.y)**2) #distance from food
            if d1 <= E_per_N:
                fight = False
                for a in a_list:
                    d2 = np.sqrt((a.x - n.x)**2+(a.y - n.y)**2) #distance of other animals from food
                    if d2 <= d1:
                        aggr_prob = np.random.randint(0,11) #here is decided whether there will be a fight or not, the higher the aggressivity the higher the probability
                        if aggr_prob <= self.aggressivity:
                            fight = True
                            n_fights += 1
                            if self.aggressivity > a.aggressivity or a.energy <= 0 or a.alive == False: #checks if the defender is alive and what aggressivity it has
                                if n in n_list:
                                    a.energy -= energy_to_fight #energy cost of the fight for the loser
                                    self.energy -= d1 #energy used to get to the food
                                    self.energy += E_per_N
                                    eaten_count += 1
                                    n_list.remove(n) #the chunk of food is removed
                            else:
                                self.energy -= energy_to_fight
                if fight == False:
                    self.energy += E_per_N
                    self.energy -= d1
                    n_list.remove(n)
                    eaten_count +=1
        self.energy -= energy_loss_per_step #at every iterations animals consume energy to simply stay alive
        return [eaten_count, n_fights]

    def change_position(self):#used to move the animal
        self.x = np.random.rand() * 500
        self.y = np.random.rand() * 500



a_list = [Animal(np.random.randint(0,501),np.random.randint(0,501), starting_energy, np.random.randint(0,11)) for i in range (number_of_animals)]



generations = []
time = []
for i in range (100):
    generations.append(len(a_list))
    time.append(i) #updating lists to make a plot
    eaten = 0
    fights = 0
    for animal in a_list:
        if animal.energy > 0: #check if the animal is dead
            pass_var = animal.catch(a_list)
            eaten += pass_var[0]
            fights += pass_var[1]
        else:
            animal.alive = False #kills the animal if the energy is less than 0
            a_list.remove(animal)

    for j,anim in enumerate(a_list):
        if anim.energy <= 0 or anim.alive == False:
            a_list.remove(anim) #this removes dead animals
        else:
            anim.change_position()

    new_borns = []
    for anim in a_list:
        if anim.energy >= energy_to_reproduce:
            new_borns.append(Animal(np.random.randint(0, 501), np.random.randint(0, 501), starting_energy, np.random.randint(0, 11)))
            anim.energy -= energy_to_reproduce #if the animal has enough energy it will use it to reproduce

    a_list += new_borns #updating animal list

    next_gen = len(a_list)
    n_list = [Nutrient(np.random.randint(0, 501), np.random.randint(0, 501)) for i in range(number_of_nutrients)]
    #regenerating nutrients
    print(f'individuals:  {next_gen}   eaten:  {eaten}  fights:  {fights}')

plt.plot(time, generations)
plt.show()




