#Program to calculate the Stefan Boltzmann constant
from scipy.integrate import quad
import numpy as np

#provided constants. hbar- Plank's constant, boltz- Boltz constant, c- Speed of light
hbar = 1.054571e-34
boltz = 1.380649e-23
c = 2.99792e8

#Function to perform integration
def Integration(x):
    t1 = x**3
    t2 = np.exp(x) - 1
    integral_value = t1/t2
    return integral_value

# integrating the function from 0 to infinity
integral_val, err=quad(Integration, 0, np.inf)

#Calculating the Stefan-Boltzmann constant
t3 = boltz ** 4 * integral_val
t4 = 4 * np.pi ** 2 * c ** 2 * hbar ** 3
Stefan_Boltzmann_constant = t3 / t4

#Formatting the Stefan-Boltzmann constant
Stefan_Boltzmann_constant = '{:.3e}'.format(Stefan_Boltzmann_constant)

print("The Stefan Boltzmann constant is,",Stefan_Boltzmann_constant)