#Printing the Prime numbers from 1 to 10000

#Import the math package to perform sqrt() function
import math

#Pass the number and the list of prime numbers to check if the number is prime
def check_prime(n, prime_list):

#If the temp value remains 0, then the number passed is a prime number
    temp = 0
    for i in prime_list:
        if int(math.sqrt(n)) != 1 :
#It's enough to check until the square root of the number to find if it is prime or not
            if i > int(math.sqrt(n)) :
                break
            else:
#If the number gives a remainder 0 when divided by any other number, it is not prime and temp is incremented
                if n % i == 0 :
                    temp+=1
#If temp remains 0, then the number is prime
    if temp == 0 :
        prime_list.append(n)

#List of prime numbers, containing only 2 at the beginning
prime_list = [2]
#The maximum value until which to print all the prime numbers
max = 10000

for i in range(3, max + 1):
    if int(math.sqrt(i) != 1):
        check_prime(i, prime_list)

print(prime_list)