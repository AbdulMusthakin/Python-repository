# This is a text based rpg game that I am working on. It is a work in progress.

import random
import time

# This is the main menu that the player will see when they start the game.
def main_menu():
    print("Welcome to the game!")
    print("Please select an option:")
    print("1. Start game")
    print("2. Exit game")
    print("3. View credits")
    print("4. View help")
    print("5. View high scores")
    print("6. View settings")
    print("7. View achievements")
    print("8. View stats")
    print("9. View inventory")
    print("10. View quests")

    user_input = input("> ")

    if user_input == "1":
        start_game()
    elif user_input == "2":
        exit_game()
    elif user_input == "3":
        view_credits()
    elif user_input == "4":
        view_help()
    elif user_input == "5":
        view_high_scores()
    elif user_input == "6":
        view_settings()
    elif user_input == "7":
        view_achievements()
    elif user_input == "8":
        view_stats()
    elif user_input == "9":
        view_inventory()
    elif user_input == "10":
        view_quests()
    else:
        print("Sorry, that is not a valid option. Please try again.")
        main_menu()