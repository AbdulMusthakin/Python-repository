from time import sleep
import random
from pwinput import pwinput  # If using program in IDLE then use getpass instead


choices = ["rock", "paper", "scissors"]
winning_choices = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
# Key is the losing choice, value is the winning choice


def play_with_someone():
    print("You have chosen to play with someone else.")
    print("How many rounds do you want to play?")

    while True:
        try:
            rounds = int(input("> "))
            sleep(1)
            if rounds < 1:
                print("You must play at least one round.")
                sleep(1)
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please try again.")
            sleep(1)

    player1_score = 0
    player2_score = 0

    while rounds != 0:
        print(f"Player 1: {player1_score} | Player 2: {player2_score}")
        print(f"Rounds left: {rounds}")
        print()
        sleep(1)

        round_is_running = True
        while round_is_running:
            print("Player 1, choose rock, paper, or scissors.")
            while True:
                try:
                    player1_choice = pwinput("> ").lower()
                    if player1_choice in choices:
                        sleep(1)
                        break
                except ValueError:
                    print("Invalid input. Please try again.")
                    sleep(1)

            print("Player 2, choose rock, paper, or scissors.")
            while True:
                try:
                    player2_choice = pwinput("> ").lower()
                    if player2_choice in choices:
                        sleep(1)
                        break
                except ValueError:
                    print("Invalid input. Please try again.")
                    sleep(1)

            print()
            print(f"Player 1 has chosen: {player1_choice}")
            print(f"Player 2 has chosen: {player2_choice}")
            print()

            if player1_choice == "rock":
                if player2_choice == "paper":
                    print("Player 2 wins this round!")
                    player2_score += 1
                    rounds -= 1
                    round_is_running = False
                elif player2_choice == "scissors":
                    print("Player 1 wins this round!")
                    player1_score += 1
                    rounds -= 1
                    round_is_running = False
                else:
                    print("It's a tie!")

            if player1_choice == "paper":
                if player2_choice == "scissors":
                    print("Player 2 wins this round!")
                    player2_score += 1
                    rounds -= 1
                    round_is_running = False
                elif player2_choice == "rock":
                    print("Player 1 wins this round!")
                    player1_score += 1
                    rounds -= 1
                    round_is_running = False
                else:
                    print("It's a tie!")

            if player1_choice == "scissors":
                if player2_choice == "rock":
                    print("Player 2 wins this round!")
                    player2_score += 1
                    rounds -= 1
                    round_is_running = False
                elif player2_choice == "paper":
                    print("Player 1 wins this round!")
                    player1_score += 1
                    rounds -= 1
                    round_is_running = False
                else:
                    print("It's a tie!")

    print("The game is over!")
    print()

    if player1_score > player2_score:
        print("Player 1 wins!")
    elif player1_score < player2_score:
        print("Player 2 wins!")
    else:
        print("It's a tie!")

    sleep(1)
    print("Returning to main menu...")
    sleep(1)
    main()


def play_with_computer():
    print("You have chosen to play with the computer.")
    print("Select a difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Impossible")

    while True:
        try:
            difficulty_choice = input("> ")
            sleep(1)

            if difficulty_choice == "1":
                difficulty = 1
            elif difficulty_choice == "2":
                difficulty = 2
            elif difficulty_choice == "3":
                difficulty = 3
            elif difficulty_choice == "4":
                difficulty = 4
            else:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please try again.")
            sleep(1)

    print("How many rounds do you want to play?")

    while True:
        try:
            rounds = int(input("> "))
            sleep(1)
            if rounds < 1:
                print("You must play at least one round.")
                sleep(1)
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please try again.")
            sleep(1)

    player_score = 0
    computer_score = 0

    while rounds != 0:
        print(f"You: {player_score} | Computer: {computer_score}")
        print(f"Rounds left: {rounds}")
        print()
        sleep(1)

        game_is_running = True
        player_choice = ""
        while game_is_running:
            print("Player 1, choose rock, paper, or scissors.")
            while True:
                try:
                    player_choice = input("> ").lower()
                    if player_choice in choices:
                        sleep(1)
                        break
                except ValueError:
                    print("Invalid input. Please try again.")
                    sleep(1)

            print("Computer is choosing...")
            sleep(1)

            if difficulty == 1:
                choices_copy = choices.copy()
                choices_copy.extend(choices)
                choices_copy.remove(winning_choices[player_choice])
                computer_choice = random.choice(choices)
            elif difficulty == 2:
                computer_choice = random.choice(choices)
            elif difficulty == 3:
                choices_copy = choices.copy()
                choices_copy.remove(winning_choices[player_choice])
                computer_choice = random.choice(choices_copy)
            else:
                computer_choice = winning_choices[player_choice]

            print(f"Computer has chosen: {computer_choice}")
            print()
            sleep(1)

            if player_choice == "rock":
                if computer_choice == "paper":
                    print("Computer wins this round!")
                    computer_score += 1
                    rounds -= 1
                    game_is_running = False
                elif computer_choice == "scissors":
                    print("You win this round!")
                    player_score += 1
                    rounds -= 1
                    game_is_running = False
                else:
                    print("It's a tie!")
            if player_choice == "paper":
                if computer_choice == "scissors":
                    print("Computer wins this round!")
                    computer_score += 1
                    rounds -= 1
                    game_is_running = False
                elif computer_choice == "rock":
                    print("You win this round!")
                    player_score += 1
                    rounds -= 1
                    game_is_running = False
                else:
                    print("It's a tie!")
            if player_choice == "scissors":
                if computer_choice == "rock":
                    print("Computer wins this round!")
                    computer_score += 1
                    rounds -= 1
                    game_is_running = False
                elif computer_choice == "paper":
                    print("You win this round!")
                    player_score += 1
                    rounds -= 1
                    game_is_running = False
                else:
                    print("It's a tie!")

    print("The game is over!")
    print()

    if player_score > computer_score:
        print("Player 1 wins!")
    elif player_score < computer_score:
        print("Computer wins!")
    else:
        print("It's a tie!")

    sleep(1)
    print("Returning to main menu...")
    sleep(1)
    main()


def main():
    print("Welcome to Rock, Paper, Scissors!")
    print(
        "The rules are simple: Rock beats Scissors, Scissors beats Paper, and Paper beats Rock."
    )

    print("Do you want to play with some else or the computer?")
    print("1. Play with someone else")
    print("2. Play with the computer")
    print("3. Quit")

    user_input = input("> ")
    sleep(1)

    if user_input == "1":
        play_with_someone()
    elif user_input == "2":
        play_with_computer()
    elif user_input == "3":
        exit()
    else:
        ("Invalid input. Please try again.")
        sleep(1)


if __name__ == "__main__":
    main()
