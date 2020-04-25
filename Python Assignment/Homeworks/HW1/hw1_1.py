#This program calculates the time taken for a ball to land when thrown from the top of a tower with height h, and initial velocity u

#Import the math package to perform sqrt() function
import math

#Get initial velocity and height as the parameters to calculate the time
def calculate_time(u, h):
#The acceleration due to gravity, is the acceleration here and its value is 9.81 m/s**2
    g = 9.81
#Calculate the time using the quadratic formula
    temp1 = 2 * g * h
    temp2 = u * u
    temp3 = math.sqrt(temp2 + temp1)
    t = (u + temp3) / g
    return t

#Get the height from the user
h = float(input("enter height: "))
#If the height entered is outside the range, display an error message
if(h<10 or h>1000):
    print("Bad height specified. Please try again.")
#If the correct height within the range is specified, get the initial velocity
else:
    v0 = float(input("enter initial upward velocity: "))
#If the initial velocity is too high or too low, display an error message
    if(v0<-20 or v0>20):
        print("Initial velocity is too large! Slow down!")
#If the initial velocity lies within the range, calculate the time and print the output
    else:
        time_print = "time to hit ground {} seconds".format(round(calculate_time(v0,h),2))
        print(time_print)