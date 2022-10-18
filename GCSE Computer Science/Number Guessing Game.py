import random
from time import sleep

difficultylist = ["easy","medium","hard","impossible"]
def intro():
    print(f"Hello, welcome to my number guessing game.\nYou will guess a number and be told if it's the correct one.\nThis is a very skill-reliant game so try your best and have fun!")
leaderboard = {
"Bert" : 2,
"Tim" : 4,
"Bartholamew" : 5,
"Bob" : 99,
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
sleep(1)

if lives > 0:
    print(f"You guessed the right number! And you only needed {5 - lives} tries")
else: print(f"You ran out of tries. The answer was {x}")
sleep(1)
print("This game has been completed by other people as well,\nYou will be showed the leaderboard with your score added in a second")
sleep(1)
name = input("Please enter your name:")
leaderboard[f"{name}"] = lives

sortedleaderboard = dict(sorted(leaderboard.items(), key = lambda x:x[1])) 
"""
The above variable is a dictionary (It's been set as that wiht the dict() method).
Its been sorted with sorted() function.
the items() method is used to extract the items from the dictionary.
The lambda function has x[1] because that it is the index of the value part of the items.
"""
sleep(2)
print(sortedleaderboard)