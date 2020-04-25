#To calculate the factorial, catalan value and GCD of the given numbers using recursion

#Recursive function to calculate the factorial of a given number
def factorial(f):
    if f==1:
        return 1
    else:
        return f*factorial(f-1)

#Recursive function to calculate the catalan value of a given number
def catalan(n):
    if n == 0 or n == 1:
        return 1
    catalan=[]

    for i in range(n+1):
        catalan.append(0)

    catalan[0] = 1
    catalan[1] = 1

    for i in range(2, n+1):
        catalan[i] = 0
        for j in range(i):
            catalan[i] = catalan[i] + catalan[j] * catalan[i-j-1]

    return catalan[n]

#Recursive function to calculate the GCD of 2 given numbers
def GCD(l,m):
	if m==0 :
		return l
	else:
		return GCD(m, l%m)

#Getting the inputs from the user
fact = int(input("Enter an integer for a factorial computation: "))
catalan_num=int(input("Enter an integer for a Catalan number computation: "))
gcd_num1 = int(input("Enter the first of two integers for a GCD calculation: "))
gcd_num2 = int(input("Enter the second integer for the GCD calculation: "))

#Calculating the output values and formatting them
fact_print = "\nfactorial of {} is {}".format(fact, factorial(fact))
catalan_print = "catalan value of {} is {}".format(catalan_num, round(float(catalan(catalan_num)),1))
gcd_print = "greatest common divisor of {} and {} is {}".format(gcd_num1,gcd_num2,GCD(gcd_num1, gcd_num2))

#Printing the output
print(fact_print)
print(catalan_print)
print(gcd_print)