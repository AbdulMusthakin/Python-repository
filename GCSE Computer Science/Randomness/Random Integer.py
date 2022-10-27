from random import randint
from time import sleep


number = randint(5,10) # random number between 5 and 10
print(f"A random number: {number}")
sleep(1)
while True: 
    input("press enter to roll:")
    x = randint(1,6)
    print(f"You rolled a {x}!")
