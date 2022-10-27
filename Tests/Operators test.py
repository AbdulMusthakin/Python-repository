import math
from numbers import Integral
import numpy

def f(z):
        return math.factorial(z) 
x = 4
y = 5
print(f"The sum of 4 and 5 is {x + y}")
print(f"Give me a number and I will give you the factorial of it")
try:
    z = int(input()) 
    print(f"The factorial of {z} is {f(z)}")
except ValueError:
    print("You need to enter a non-negative integer")
    z = int(input())
    print(f"The factorial of {z} is {f(z)}")