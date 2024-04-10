from tkinter import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import datetime #used to print date on screen

background = 'brown'
foreground = 'yellow'
window = Tk() #creates window
window.title('Logistic map')
window.geometry('700x720')
window.config(bg = background)

#here the initial conditions are asked
label1 = Label(window, text = 'Insert initial conditions (0 - 1)', pady = 5, bg = background, fg = foreground).pack(side=TOP)
initial_conditions = Entry(window)
initial_conditions.insert(0,0.2) #puts inside the entry widget the value 0.2, so when you run the program you see this as prewritten value
initial_conditions.pack(side=TOP) #these are respectively the first piece of text and the first space where you can enter an input

#here the growth rate is asked, same considerations as the initial conditions section
label2 = Label(window,text = 'insert the r value (0 - 4)', pady = 5, bg = background, fg = foreground).pack(side=TOP)
r_input = Entry(window)
r_input.insert(0,1.4)
r_input.pack(side=TOP)

#same stuff but for the number of iterations
label3 = Label(window, text = 'insert the number of iterations', pady = 5, bg = background, fg = foreground).pack(side=TOP)
iterations_input = Entry(window)
iterations_input.insert(0,50)
iterations_input.pack(side=TOP)

fig = plt.Figure() #creates a matplotlib figure that will be updated every time the button is pushed
canvas = FigureCanvasTkAgg(fig, window) #creates canvas, like the figure it will be updated every time the button is pressed
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=TOP, expand=False, pady=5) #packs canvas
toolbar = NavigationToolbar2Tk(canvas, window) #adds the useful matplotlib toolbar

#displaying graph section
def graph():
    #this is the function linked to the button

    #in this section the inputs are taken from the entry widgets
    R = float(r_input.get())
    x0 = float(initial_conditions.get())
    iterations = int(iterations_input.get())

    #in this section the population is calculated as many times as the iterations the user specified
    t = [k for k in range(iterations+1)] #time
    p = [] #population list
    population = x0
    p.append(population) #adds the initial populations at t = 0
    for i in range(iterations): # in reality there are iterations + 1 values because I already added the t = 0 and the initial conditions
        population = R * population * (1 - population)
        p.append(population)

    #in this section the figure object and the canvas are updated
    fig.clear()
    ax = fig.add_subplot(111)
    ax.grid()
    ax.set_xlim(0,iterations)
    ax.set_ylim(0,1.1)
    ax.set_ylabel('population')
    ax.set_xlabel('generations')
    ax.plot(t,p, marker = '.')
    canvas.draw_idle()

graph_button = Button(window, text = 'graph', command = graph, cursor = 'hand2') #power button
graph_button.pack(side=BOTTOM)


#displaying date section
time_label = Label(window, bg = background, fg = foreground) #creates a new label with nothing inside
time_label.pack(side=BOTTOM)
def update_date():
    #this function updates the label and the date
    today_date = datetime.datetime.now() #takes date and time in this moment
    string_date = today_date.strftime('%B %d, %Y  %H:%M:%S') #converts data taken in string using string formatting
    time_label.config(text=string_date) #updates label
    window.after(1000,update_date) #this updates the window and reruns the update_date function after a second(1000 ms)
update_date()

window.mainloop()