# Project 3 - Find the current through the diode and optimize the values of the resistor, IDE and PHI
from scipy.optimize import fsolve
import numpy as np
from scipy import optimize
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Ignore the warnings
warnings.filterwarnings("ignore")

################################################################################
#                                                                              #
# Problem 1: Determining the current through the diode using the given formula #
#                                                                              #
################################################################################

# Function to solve the diode voltage and get the error
def Diode_V(vd,vs,r,n,t,Io):
    current = Diode_current(vd,n,t, Io)
    err = (vd-vs)/r + current
    return(err)
# Function to calculate the diode current
def Diode_current(vd,n,t,Io):
    vt = n*k*t/q
    return(Io*(np.exp(vd/vt)-1))

# Assign the initial values to the variables
R1 = 11e3           # Value of the resistor
Io = 1e-9           # Saturation current
Vt = 0.05           # Threshold voltage of the diode
n = 1.7             # Exponential ideality factor
T = 350             # Absolute temperature
k = 1.380648e-23    # Boltzmann constant
q = 1.6021e-19      # Charge of the electron

temp = (n*k*T)/q    # Calculated for easier calculation of the diode current

V_diode = []        # Empty array to store voltages
I_diode = []        # Empty array to store current
Err_diode = []      # Empty array to store the errors

def f(v):
    Id = Io * (np.exp(v * q / (n * k * T)) - 1.0)      # current through the diode
    a = (v-Vs) / R1 + Id                               # solve node
    return a

# The source voltage increments by 0.1
volt_src=np.arange(0.1,2.6,0.1)
print('The source voltages are: ', volt_src)

# Solve for the values of Vs and store them
for Vs in volt_src :
    g = fsolve(f,1)
    V_diode.append(g[0])

# Calculate the current across the diode
for i in range(0,len(V_diode)):
    # print(round(V_diode[i],3))
    current = Io * ((np.exp(V_diode[i] / temp)) - 1)    #Calculate the value of the current
    I_diode.append(current)                             #Store the calculated current value in the array

# Calculate the errors in the diode
for i in range(len(volt_src)):
    b = (V_diode[i] - volt_src[i] ) / R1
    Err_diode.append(b + I_diode[i])

# Print the voltage across the diode
print('voltage through the diode:\n', V_diode)

# Print the current across the diode
print('Current through the diode:\n', I_diode)

# Print the maximum voltage and the maximum current across the diode
print('Maximum Voltage through the diode:\n', max(V_diode))
print('Maximum Current through the diode:\n', max(I_diode))

# Print the errors encountered
print('Errors:\n', Err_diode)

# Plot the graph
fig=plt.figure()
ax= fig.add_subplot(2,1,1)
ax.plot(V_diode,I_diode)
ax.plot(volt_src,I_diode)
plt.ylabel('Diode Current VS Source Voltage')
plt.xlabel('Diode Voltage VS Source Current')
ax.set_yscale('log')
plt.grid()
plt.show()

##################################################################################
#                                                                                #
# Problem 2:                                                                     #
#  A. Adding a diode with the new given value in the circuit, calculate the new  #
#     Current array                                                              #
#  B. Find the missing parameters(n, phi, r)                                     #
#                                                                                #
##################################################################################

# Assigning the values to the variables
A = 1e-8              # Area of the diode
T = 375                 # Temperature in K
int_R   = 10e3          # Initial value of Resistor
int_phi = 0.8           # Initial value of Phi
int_IDE = 1.5           # Initial value of Ideality
limit = 1000            # Maximum iterations limit
err_limit  = 1e-3       # Error limit
P1_VDD_STEP = 0.1       # Voltage step value

# Loading the DiodeIV.txt
def data(file_name):
    df = pd.read_csv(file_name,sep=' ',header=None)
    source_v = df.iloc[:,0].values
    diode_i  = df.iloc[:,1].values
    return source_v, diode_i

################################################################################
# The following functions does the optimization for the resistor, IDE and PHI  #
# Inputs:                                                                      #
#    r_value   - value of the resistor                                         #
#    ide_value - value of the ideality                                         #
#    phi_value - value of phi                                                  #
#    area      - area of the diode                                             #
#    temp      - temperature                                                   #
#    src_v     - source voltage                                                #
#    meas_i    - measured current                                              #
# Outputs:                                                                     #
#    err_array - array of error measurements                                   #
################################################################################

# Optimization of resistor
def opt_r(r_value,ide_value,phi_value,area,temp,src_v,meas_i):
    est_v   = np.zeros_like(src_v)       # an array to hold the diode voltages
    diode_i = np.zeros_like(src_v)       # an array to hold the diode currents
    prev_v = P1_VDD_STEP                 # an initial guess for the voltage

    # need to compute the reverse bias saturation current for this phi!
    is_value = area * temp * temp * np.exp(-phi_value * q / ( k * temp ) )

    for index in range(len(src_v)):
        prev_v = optimize.fsolve(Diode_V,prev_v,
                                (src_v[index],r_value,ide_value,temp,is_value),
                                xtol=1e-12)[0]
        est_v[index] = prev_v            # store for error analysis

    # compute the diode current
    diode_i = Diode_current(est_v,ide_value,temp,is_value)
    return (meas_i - diode_i )


# Optimization of Ideality
def opt_ide(ide_value,r_value,phi_value,area,temp,src_v,meas_i):
    est_v   = np.zeros_like(src_v)       # An array to hold the diode voltages
    diode_i = np.zeros_like(src_v)       # An array to hold the diode currents
    prev_v = P1_VDD_STEP                 # An initial guess for the voltage

    # need to compute the reverse bias saturation current for this phi!
    is_value = area * temp * temp * np.exp(-phi_value * q / ( k * temp ) )

    for index in range(len(src_v)):
        prev_v = optimize.fsolve(Diode_V,prev_v,
                                (src_v[index],r_value,ide_value,temp,is_value),
                                xtol=1e-12)[0]
        est_v[index] = prev_v            # store the values for future use in analysing the error

    # compute the diode current
    diode_i = Diode_current(est_v,ide_value,temp,is_value)
    return (meas_i - diode_i +1e-30 )/(meas_i + diode_i +1e-30)

# Optimization of PHI
def opt_phi(phi_value,r_value,ide_value,area,temp,src_v,meas_i):
    est_v   = np.zeros_like(src_v)       # an array to hold the diode voltages
    diode_i = np.zeros_like(src_v)       # an array to hold the diode currents
    prev_v = P1_VDD_STEP                 # an initial guess for the voltage

    # need to compute the reverse bias saturation current for this phi!
    is_value = area * temp * temp * np.exp(-phi_value * q / ( k * temp ) )

    for index in range(len(src_v)):
        prev_v = optimize.fsolve(Diode_V,prev_v,
                                (src_v[index],r_value,ide_value,temp,is_value),
                                xtol=1e-12)[0]
        est_v[index] = prev_v            # store for error analysis

    # compute the diode current
    diode_i = Diode_current(est_v,ide_value,temp,is_value)
    return (meas_i - diode_i +1e-30 )/(meas_i + diode_i +1e-30)

source_v, meas_diode_i = data("DiodeIV.txt")  # passing the input file

# Initialize some values to the variables
r_val   = int_R                         # Initial resistor value
phi_val = int_phi                       # Initial PHI value
ide_val = int_IDE                       # Initial IDE value
est_v = np.zeros_like(source_v)         # Array for voltage
diode_i = np.zeros_like(source_v)       # Array for currents
prev_v = P1_VDD_STEP

for i in range(limit):
# Optimization of the Resistor value
    r_val_opt = optimize.leastsq(opt_r, r_val, args = (ide_val, phi_val, A, T, source_v, meas_diode_i))
    store_r_v = r_val
    r_val = r_val_opt[0][0]

# Optimization of the PHI value
    phi_val_opt = optimize.leastsq(opt_phi, phi_val, args = (r_val, ide_val, A, T, source_v, meas_diode_i))
    store_phi_v = phi_val
    phi_val = phi_val_opt[0][0]

# Optimization of the IDE value
    ide_val_opt = optimize.leastsq(opt_ide, ide_val, args = (r_val, phi_val, A, T, source_v, meas_diode_i))
    store_ide_v = ide_val
    ide_val = ide_val_opt[0][0]

# Calculating the residual and error
    residual = opt_r(phi_val,r_val,ide_val,A,T,source_v,meas_diode_i)
    error = np.sum(np.abs(residual))/len(residual)  ## calculating error from them.

# Print the optimized values of the resistor, ideality and phi value
    print("Iteration number: ", i)
    print("Resistor:", r_val)
    print("Ideality:", ide_val)
    print("PHI value:", phi_val)
    if error < (err_limit) or (store_r_v==r_val and store_ide_v==ide_val and store_phi_v==phi_val):
        break
is_value = A * T * T * np.exp(-phi_val * q / ( k * T ) )
# Calculating the diode current value for plotting it by using all the optimized values.
for index in range(len(source_v)):
    prev_v = optimize.fsolve(Diode_V, prev_v, (source_v[index], r_val, ide_val, T, is_value), xtol=1e-12)[0]
    est_v[index] = prev_v            # store for error analysis

# Compute the current in the diode
diode_i = Diode_current(est_v, ide_val, T, is_value)

# Plot the graph
p1 = plt.subplot()
p2 = p1.twinx()
p1.plot(source_v,np.log10(meas_diode_i+1e-10),'r-')
p2.plot(source_v,np.log10(diode_i+1e-10),'b-')
plt.grid()
p1.set_ylabel('Diode Current vs Source Voltage (log scale)')
p2.set_ylabel('Diode Current vs Source Voltage (log scale)')
p1.set_xlabel('Voltage')
plt.show()
