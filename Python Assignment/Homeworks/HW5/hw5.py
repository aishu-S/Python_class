# Problem 1: y’ = cos(t); initial value: y(0)=1
# Problem 2: y’ = -2y + (2t+1)*np.exp(-2t); initial value y(0) = 0
# Problem 3: y” = -28cos(2t) + 3sin(2t)– 3y’ + y; initial values y(0) = 2, y’(0) = -6

# Import the packages
import numpy as np                   # To solve for cos, sin and exp values
import matplotlib.pyplot as plt      # To plot the graphs
from scipy.integrate import odeint   # This is the ODE solver

time_vec = np.linspace(0, 7, 700)              # create the time steps

## Problem 1
# Define the ODE function
def prob_1(ypos, time):
    return np.cos(time)

# Call the ODE function with initial value y(0) = 1
yvec_1 = odeint(prob_1, 1, time_vec)

# Plot the graph of the output
plt.plot(time_vec, yvec_1)
plt.xlabel('time')
plt.ylabel('y')
plt.show()

## Problem 2
# Define the ODE function
def prob_2(ypos, time):
    return (-2 * ypos) + ((2 * time) + 1) * np.exp(-2 * time)

# Call the ODE function with initial value y(0) = 0
yvec_2 = odeint(prob_2, 0, time_vec)

# Plot the graph of the output
plt.plot(time_vec, yvec_2)
plt.xlabel('time')
plt.ylabel('y')
plt.show()

## Problem 3
# Define the ODE function
def prob_3(ypos, time):
    return [ypos[1], -28*np.cos(2*time) + 3*np.sin(2*time) - 3*ypos[1] + ypos[0]]

# Call the ODE function with initial values y(0) = 2, y’(0) = -6
y_values_3 = [2, -6]
yvec_3 = odeint(prob_3, y_values_3, time_vec)

# Plot the graph
plt.plot(time_vec,yvec_3)
plt.title('Problem 3')
plt.xlabel('time')
plt.ylabel('y')
plt.gca().legend(('y vs t',"y' vs t"))
plt.show()