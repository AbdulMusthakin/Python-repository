import random

difficultylist = ["easy","medium","hard","impossible"]
def intro():
    print(f"Hello, welcome to my number guessing game.\nYou will guess a number and be told if it's the correct one.\nThis is a very skill-reliant game so try your best and have fun!")


lives = 5
guess = 0
intro()

x = 0
y = input(f"Choose a difficulty(Easy, Medium, Hard, Impossible):") # To Be Finished
while y.lower in difficultylist:
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
print (f"You have {lives} lives left.") if guess != x else x
while guess != x and lives > 0:
    guess = int(input(f"Try again:"))
    lives -= 1 if guess != x else x
    if guess > x:
        print(f"Your guess was too high")
    elif guess < x:
        print(f"Your guess was too low")
    else: pass
    print(f"You have {lives} lives left.") if lives > 0 and guess != x else x


if lives > 0:
    print(f"You guessed the right number!")
else: print(f"You ran out of tries. The answer was {x}")
