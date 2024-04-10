import matplotlib.pyplot as plt
import random

wound_damage = 100
flee_damage = 0
loss_of_time_damage = 11
win_energy = 50
starting_energy = 1000
reproduction_energy = 2000
energy_loss_per_turn = 10
max_animali = 500
class Animal:
    def __init__(self, type, energy):
        self.type = type
        self.energy = energy
        self.alive = True
    def fight(self, an2):
        if self.type == 'F':
            if an2.type == 'C':
                self.energy += win_energy
            else:
                w = random.randint(0,1)
                if w == 0:
                    an2.energy -= wound_damage
                    self.energy -= wound_damage
                    self.energy += win_energy
                else:
                    self.energy -= wound_damage
                    an2.energy -= wound_damage
                    an2.energy += win_energy

        else:
            if an2.type == 'F':
                self.energy -= flee_damage
            else:
                w = random.randint(0, 1)
                if w == 0:
                    an2.energy -= loss_of_time_damage
                    self.energy -= loss_of_time_damage
                    self.energy += win_energy
                else:
                    self.energy -= loss_of_time_damage
                    an2.energy -= loss_of_time_damage
                    an2.energy += win_energy


f_list = [Animal('F',starting_energy) for i in range(300)]
c_list = [Animal('C', starting_energy) for i in range (1000)]
animals_list = f_list + c_list

colombe = []
falchi = []
time = []
for i in range (10000): #the number in the range is the number of iterations
    numbers_list = [i for i in range (len(animals_list))] #creates a list of numbers to easier access the animals in the list
    #and make them fight without repetiotion (every animal fights exactly 1 time)
    time.append(i) #used to take data

    f_c_encounters = 0
    f_f_encounters = 0
    for j in range(int(len(animals_list)/2)): #the number in range is half of the total population rounded by defect
        a1 = random.choice(numbers_list)
        numbers_list.remove(a1)

        a2 = random.choice(numbers_list)
        numbers_list.remove(a2)
        animals_list[a1].fight(animals_list[a2])
        if animals_list[a1].type == 'F' and animals_list[a2].type == 'F':
            f_f_encounters+=1
        elif animals_list[a1].type == 'F' and animals_list[a2].type == 'C' or animals_list[a1].type == 'C' and animals_list[a2].type == 'F':
            f_c_encounters +=1

    print(f_f_encounters, '   ', f_c_encounters)
    numero_falchi = 0 #used to take data
    numero_colombe = 0 #used to take data
    dead_animals = 0
    for an in animals_list:
        an.energy -= energy_loss_per_turn

        if an.type == 'F':
            numero_falchi += 1
        else:
            numero_colombe += 1

        if an.energy <= 0:
            an.alive = False
            dead_animals += 1
        elif an.energy > reproduction_energy and len(animals_list) <= max_animali:
            an.energy -= reproduction_energy
            animals_list.append(Animal(an.type, starting_energy))
            pass
    #animals_list = [animals_list[k] for k in range(len(animals_list)) if animals_list[k].alive == True]
    falchi.append(numero_falchi)
    colombe.append(numero_colombe)
    #print(f'F: {numero_falchi},  C: {numero_colombe},  TOT: {len(animals_list)}')
    next_gen = []
    for h in range(len(animals_list)):
        if animals_list[h].alive == True:
            next_gen.append(animals_list[h])
    animals_list.clear()
    animals_list = next_gen

    random.shuffle(animals_list)
'''    for z in range(dead_animals):
        t = random.randint(0,1)
        if t == 0:
            a = Animal('C', starting_energy)
        else:
            a = Animal('F', starting_energy)
        animals_list.append(a)'''

plt.plot(time,colombe, color = 'green', label = 'colombe', marker = 'x')
plt.plot(time,falchi, color = 'red', label = 'falchi', marker = '.')
plt.grid()
plt.legend(loc='best')
plt.show()
