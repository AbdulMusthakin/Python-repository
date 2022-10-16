import random
from time import sleep

difficultylist = ["easy","medium","hard","impossible"]
def intro():
    print(f"Hello, welcome to my number guessing game.\nYou will guess a number and be told if it's the correct one.\nThis is a very skill-reliant game so try your best and have fun!")
leaderboard = { # To be Finished
"Bert" : 2,
"Tim" : 4,
"Bartholamew" : 5,
} 

lives = 5
guess = 0
intro()

x = 0
y = "None"
while y.lower() not in difficultylist:
    y = input(f"Choose a difficulty(Easy, Medium, Hard, Impossible):")
    if y.lower() == "easy":
        x = random.randint(1, 10)
    elif y.lower() == "medium":
        x = random.randint(1, 20)
    elif y.lower() == "hard":
        x = random.randint(1, 50)
    elif y.lower() == "impossible":
        x = random.randint(1, 1000)


guess = int(input(f"Guess the Number:"))
if guess != x:
    lives -=1
if guess > x:
    print(f"Your guess was too high")
elif guess < x:
    print(f"Your guess was too low")
else: pass
if guess != x:
    print (f"You have {lives} lives left.")
while guess != x and lives > 0:
    guess = int(input(f"Try again:"))
    if guess != x:
        lives -= 1
    if guess > x:
        print(f"Your guess was too high")
    elif guess < x:
        print(f"Your guess was too low")
    else: pass
    print(f"You have {lives} lives left.") if lives > 0 and guess != x else 0


if lives > 0:
    print(f"You guessed the right number! And you only needed {5 - lives} tries")
else: print(f"You ran out of tries. The answer was {x}")
