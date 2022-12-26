from time import sleep
from pytimedinput import timedInput


RULES = """
1. A sequence of numbers will be displayed one at a time. This will start at 1 and end at your specified max number.
2. If a number is divisible by 3, it will be replaced by 'fizz'. If its divisible by 4, by 'jazz' and if by 5, 'jazz'.
3. If it is divisible by multiple, then it will display a combination of those words in ascending order of divisbility. e.g. 'fizz' will always be first.
4. Before every number, you will be given time to enter the correct number or words. 
5. If your answer is correct then you will continue the game, otherwise it will end.

Those are all the rules. Now good luck and remember that there is a time limit for entering your answers.
"""
leaderboard = {
    "Bob" : 12,
    "Tim" : 42,
    "Bartholamew" : 3,
    "Jimmy" : 67,
    "Kim Yo Wang" : 5040,
}


def game(max_range):
    function_score = 0
    for i in range(1, max_range + 1):
        num = ""
        if i % 3 == 0:
            num += "fizz"
        if i % 4 == 0:
            num += "jazz"
        if i % 5 == 0:
            num += "buzz"
        if num == "":
            num = str(i)
        user_input = timedInput(prompt="Enter your answer: ", timeout=10)
        user_answer = user_input[0]
        if user_input[1] is True:
            print("Ran out of time. Game Over")
            function_score = i - 1
            break
        if user_answer == num:
            print("Correct")
            function_score = i
        else:
            print("Incorrect, Game Over.")
            function_score = i - 1
            break
    return function_score


def intro():
    while True:
        try:
            user_input = input("Welcome to the fizzbuzz game. \
There are a few rules to this but you can press ENTER to start the game now. \
Press 1 to read the rules. Press 2 to see the leaderboard. \
Press 3 to quit the game.")
            if user_input == "":
                user_max_value = int(input("Enter the max number you want to go upto. \n"))
                score = game(user_max_value)
                print(f"Your score is {score}")
                sleep(0.5)
                name = input("What is your first name?")
                leaderboard.update({name : score})
                sleep(0.5)
                print("You will now be returned to the intro section.")
                sleep(0.5)
                intro()
            elif user_input == "1":
                print(RULES)
                sleep(0.5)
                intro()
            elif user_input == "2":
                print(leaderboard)
                sleep(0.5)
                print("\nYou can play to add or update your name on the leaderboard. \n")
                sleep(1)
                intro()
            elif user_input == "3":
                pass
            else:
                raise ValueError
            break
        except ValueError:
            print("You have entered something which is not accepted. Try again.")
            sleep(1)



intro()
