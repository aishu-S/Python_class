############################################################
# Created on Fri Aug 24 13:36:53 2018                      #
#                                                          #
# @author: olhartin@asu.edu; updates by sdm                #
#                                                          #
# Program to solve resister network with a voltage source  #
############################################################

import numpy as np                     # needed for arrays
from numpy.linalg import solve         # needed for matrices
from read_netlist import read_netlist  # supplied function to read the netlist
import comp_constants as COMP          # needed for the common constants

# this is the list structure that we'll use to hold components:
# [ Type, Name, i, j, Value ] ; set up an index for each component's property

############################################################
# How large a matrix is needed for netlist? This could     #
# have been calculated at the same time as the netlist was #
# read in but we'll do it here to handle special cases     #
############################################################

def ranknetlist(netlist):               # pass in the netlist
    no_of_volt = 0                      #Set the number of volts to 0, increment it as we encounter voltage sources
    node_list = []                      #The node_list is used to store the components of the netlist

#Check each component in the netlist. If an item is absent, add it to the node_list
    for comp in netlist:
        if(comp[3] not in node_list):
            node_list.append(comp[3])
        if(comp[2] not in node_list):
            node_list.append(comp[2])
#if the component is a voltage source increment the number of volt
        if comp[0] == 1:
            no_of_volt +=1

#Calculate the total number of nodes and return the total number of nodes and the node list
    max_node = no_of_volt + len(node_list)-1
    return node_list,max_node

############################################################
# Function to stamp the components into the netlist        #
############################################################

def stamper(y_add,netlist,currents,voltages,num_nodes): # pass in the netlist and matrices
    # y_add is the matrix of admittances
    # netlist is the list of lists to analyze
    # currents is the vector of currents
    # voltages is the vector of voltages
    # num_nodes is the number of nodes

    for comp in netlist:                            # for each component...
        #print(' comp ', comp)                       # which one are we handling...

        # extract the i,j and fill in the matrix...
        # subtract 1 since node 0 is GND and it isn't included in the matrix

        if ( comp[COMP.TYPE] == COMP.R ):           # a resistor
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            if (i >= 0):                            # add on the diagonal
                y_add[i,i] += 1.0/comp[COMP.VAL]
            if (j >= 0) and (i >=0):                #Add resistor
                y_add[j,i] -= 1.0/comp[COMP.VAL]
            if (j >=0):                             #Left diagonal
                y_add[j,j] += 1.0/comp[COMP.VAL]
            if (i >= 0) and (j >=0):                #Add resistor
                y_add[i,j] -= 1.0/comp[COMP.VAL]

        if ( comp[COMP.TYPE] == COMP.IS ):          #Current source
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1

            if(i >= 0 ):                            #Negative current
                currents[i] -= comp[COMP.VAL]
            if( j >= 0):                            #Positive current
                currents[j] +=  comp[COMP.VAL]

        if ( comp[COMP.TYPE] == COMP.VS ):          #Voltage source
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1

            if (i >= 0):
                y_add[i,num_nodes] = 1
                y_add[num_nodes,i] = 1
            if (j >= 0):
                y_add[j,num_nodes] = -1
                y_add[num_nodes,j] = -1

            currents[num_nodes] = comp[COMP.VAL]    #Add the current values
            num_nodes += 1

    return num_nodes  # need to update with new value

############################################################
# Start the main program now...                            #
############################################################
# Read the netlist!
netlist = read_netlist()

#Call ranknetlist function to get the number of nodes and the nodes in the netlist
node_list , max_node = ranknetlist ( netlist )
num_nodes= len(node_list)-1         #To exclude the voltage
#Admittance is initialized as an empty matrix
y_add  = np.zeros((max_node,max_node),dtype=float)
#Current vector is initialized as an empty array
currents = [0.] * max_node
#Voltage vector is initialized empty
voltages = [0.] * max_node
#Call the stamper function
stamper(y_add,netlist,currents,voltages,num_nodes)

#Print the voltage vector
print("Voltage vector:",solve(y_add,currents))