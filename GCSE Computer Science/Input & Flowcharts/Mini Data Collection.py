from re import A
from xmlrpc.client import boolean


print("What is your first initial?") # This asks for the initial of my first name
initial = input() # This created a variable with the value being my input to the question printed
print("What is your surname")
surname = input()
print("What is your age?")
try:
    age = int(input()) 
except ValueError:
    print("You must enter a number")
    age = int(input())
print("True or False - you like marmite")
likes_marmite = input()
marmite = "True"
decades = float((age / 10)) # sets value of of variable to be age divided by 10
print("Well hello", initial, surname)
print("It is", str(likes_marmite==marmite), "that you like marmite.") # Here it checks if one variable is equal to another and returns the string of the boolean
print("This is probably because you are", str(decades), "decades old") # returns the float variable decades as a string
print("enter a number")
