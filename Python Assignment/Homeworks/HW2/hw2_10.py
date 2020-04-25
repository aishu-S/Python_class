# Program to calculate the period of the oscillator for given amplitude a, and
# Plot a graph of the period for amplitudes ranging from a = 0 to a = 2.

#import the necessary packages for the program

from scipy.integrate import quad    #To perform integration
import numpy as np                  #To use arange to get an array with values from 0.1 to 2 with increments of 0.01
import math                         #To get square roots of values
import matplotlib.pyplot as plt     #To plot the graph

#Function to perform the integration and calculate the time at every amplitude
def integration(x, a):
    t1 = math.sqrt(8)
    t2 = a**6 + 2 * (a**2)
    t3 = x**6 - 2 * (x**2)
    t4 = t2 - t3
    t5 = math.sqrt(t4)
    t6 = 1/t5
    T = t1 * t6
    return T

#amplitude array containing values from 0.1 to 2.00
amplitudes = np.arange (0.10 , 2.01 , 0.01)
#length of the amplitudes array
points = len(amplitudes)
#an empty array to store the integrals
integral = np.zeros(points, float)

#for loop to call the integration function and calculate the time at each amplitude
for i in range(points):
    amp = amplitudes[i]
    integral[i], err = quad(integration, 0, amp, args = (amp,))

#plot the graph woth amplitudes as the x-axis and time period as the y-axis
plt.plot(amplitudes,integral)
plt.xlabel("Amplitude")
plt.ylabel("Time period")
plt.show()