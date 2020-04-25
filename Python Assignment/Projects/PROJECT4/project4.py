# Project 4- To find the optimal number of inverter and fans that produce the minimum delay

import numpy as np      # package needed to read the results file
import subprocess       # package needed to launch hspice

# Function to copy and write the contents of InvChain.sp into project4.sp and
# To calculate the delay for different values of N and fan

def Delay_calc(n, fans):

# Copying the contents up to line 36 from InvChain.sp to project4.sp

    f_ref = open("InvChain.sp","r")
    f = open("project4.sp","w")

    lines = f_ref.readlines()

    for sentence in range(0, 36):
        f.write(lines[sentence])

    f_ref.close()

# Appending the remaining contents to the project4.sp

    sentence = ".measure TRAN tphl_inv  TRIG v(Xinv1.a) VAL = 1.5 RISE = 1 TARG v(z) VAL=1.5 FALL = 1\n.param fan = " + str(fans) + "\n"
    f.write(sentence)

# Calculating the values for the inverter chain
# Using the ASCII values for the letters of the inverter chain, starting from a = 97

    next_var = 97
    count = 1
    for i in range(1, n+1):
        sentence = "Xinv" + str(i) + " " + chr(next_var) + " "

        if i == n:
            sentence += "z inv M="
        else:
            next_var += 1
            sentence += chr(next_var) + " inv M="

        if i == 1:
            sentence += "1\n"
        else:
            sentence += "fan**"+str(count)+"\n"
            count+=1

# Append the sentence to the existing project4.sp file and end it
# Close the file once everything is appended

        f.write(sentence)
    f.write(".end")
    f.close()

# The main function
# Consider 10 fans and 10 inverters
# Initially consider that the delay is 1 to calculate the minimum delay

Fan = list(range(2, 12))
N = list(range(1, 20, 2))

delay = 1.0

# Create a nested loop to calculate the delay for different value of
# the inverter with different values of the fan

for elem_N in N:
    for elem_fan in Fan:
        Delay_calc(elem_N, elem_fan)
        proc = subprocess.Popen(["hspice","project4.sp"],
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        data = np.recfromcsv("project4.mt0.csv",comments="$",skip_header=3)
        tphl = data["tphl_inv"]
        print("\nN= {}, \nfan= {}, \ndelay= {}".format(elem_N, elem_fan, tphl))

        # Calculate the optimal values which give the minimum delay
        if tphl < delay:
            N_max = elem_N
            fan_max =elem_fan
            delay = tphl

# Print the optimal values

print("\n\n#################### OPTIMAL VALUES ####################")
print("\nOptimal value for N: {}".format(N_max))
print("\nOptimal fan value: {}".format(fan_max))
print("\nMinimum delay: {}".format(delay))
