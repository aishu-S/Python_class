#Program that uses GUI to calculate your wealth at retirement with a list of inputs

from tkinter import *               #For the GUI
import matplotlib.pyplot as plt     #To plot the graph
import numpy as np

#To calculate the wealth during retirement
def Calculate_data(e1,e2,e3,e4,e5,e6):
##
##Read the values entered by the user and convert them to float values.
##Creating a config object to minimize number of parameters to functions
##
    config = {
        "r": float(e1.get()), # mean return
        "sd": float(e2.get()), # standard deviation of return
        "y": float(e3.get()), # yearly contribution
        "ny": float(e4.get()), # num of years of contribution
        "NC": float(e5.get()), # num of years to retirement
        "nr": float(e6.get()) # annual spend in retirement
    }

    run_analyses(config)

def run_analysis(config):

## Destructuring values from config object
    r = config["r"]
    sd = config["sd"]
    y = config["y"]
    ny = config["ny"]
    NC = config["NC"]
    nr = config["nr"]

    wealth = [0 for x in range(70)]
    wealth[0] = y

    #range_1 = range(1, 70-NC)
    for i in range(1, 70):
        noise = (sd/100) * np.random.uniform(-1, 1)
        wealth[i] = wealth[i-1] * (1+ (r/100) + noise)

        if ny > 0:
    #This is a year in which contribution has ocurred
            wealth[i] += y
            ny -= 1 # Decrementing number of years of contribution

        if NC == 0:
    #This is a retirement year, hence decrementing expenditure
            wealth[i] -= nr

        else:
    #Non-retirement year
            NC -= 1

        if wealth[i] < 0:
    ##Flattening out wealth after going negative
            wealth[i] = 0
            break

    return wealth

def run_analyses(config, times=10):
#Runs the calculations multiple times
    analyses = np.array([run_analysis(config) for x in range(times)]) # 2D numpy array containing 10 simulations for 70 years
    analyses_mean = analyses.mean(axis=0)  # Mean of the 10 simulations for 70 years

    retirement_year = int(config["NC"])
    mean = analyses_mean[retirement_year] # Mean of the year of retirement
    mean = round(mean, 2)
    mean_ans = str(mean)
    Label(master, text = mean).grid(row=6)
    for i in range(times):
        plt.plot(list(range(70)), analyses[i,:].T)
    plt.show()

    return analyses, analyses_mean.mean()

#Create the GUI
master = Tk()
master.title("Retirement savings calculator")
Label(master, text="Mean Return (%) ").grid(row=0)
Label(master, text="Std Dev Return (%) ").grid(row=1)
Label(master, text="Yearly Contribution ($) ").grid(row=2)
Label(master, text="No. of Years of Contribution ").grid(row=3)
Label(master, text="No. of Years to Retirement ").grid(row=4)
Label(master, text="Annual Spend in Retirement ").grid(row=5)

#Allow data entry. Create 6 data entries for the 6 data
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)

#Line up the entries with the respective labels
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)

#Create the quit button that will execute the destroy command
Button(master,text='Quit',command=master.destroy).grid(row=7, column=0, sticky=W, pady=4)
#Create the calculate button that will execute the Calculate_data function
Button(master,text='Calculate', command=lambda: Calculate_data(e1,e2,e3,e4,e5,e6)).grid(row=7, column=1)

#Run the code till the window is closed
mainloop()