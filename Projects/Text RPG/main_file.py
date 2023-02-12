# This is a text based rpg game that I am working on. It is a work in progress.

# ------------------ Importing Modules ------------------ #

import random
from time import sleep
import os


# ------------------ Setting Map ------------------ #
"""
This is the map that the player will see when they start the game.
  A B C D...
1 □ □ □ □ □
2 □ □ □ □ □
3 □ □ □ □ □
4 □ □ □ □ □
⋮ □ □ □ □ □
"""

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.visual_map = []
        self.detailed_map = {}


    def create_visual_map(self):
        for _ in range(self.height):
            self.visual_map.append(["□"] * self.width)

    def create_detailed_map(self):
        # copy the dictionary detailed_map as current_detailed_map

        for j in range(self.height):
            current_row = []
            for i in range(self.width):
                # Every time the loop runs, I want a counter to increase letter.
                # For example, the first time it will be A, then B, then C, etc.
                current_row.append([chr(i+65) + str(j + 1)])
            self.detailed_map[j+1] = current_row

        return self.detailed_map


    def print_map(self):
        for row in self.visual_map:
            print(" ".join(row))
    
    def __str__(self):
        return f"Width: {self.width}, Height: {self.height}"
    

    class Zone:
        def __init__(self, name, description="", is_player_here=False):
            self.name = name
            self.description = description
            self.is_player_here = is_player_here

        def place_player(self):
            self.is_player_here = True

        def remove_player(self):
            self.is_player_here = False

        def __str__(self):
            return f"Name: {self.name}, Description: {self.description}, Is Player Here: {self.is_player_here}"


# ------------------ Setting Character ------------------ #

class Character:
    def __init__(self, name, health, attack, defense, magic):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.level = 0
        self.exp = 0
        self.gold = 0
        self.points = 5

    def __str__(self):
        return f"Class: {self.__class__.__name__}, Name: {self.name}, Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Magic: {self.magic}, Level: {self.level}"


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 100, 15, 10, 5)


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, 75, 5, 5, 15)
    

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 50, 15, 0, 5)


classes_list = ["Warrior", "Mage", "Rogue"]    

# ------------------ Character Selection ------------------ #

def character_selection():
    name = input("What do you want your character's name to be?\n> ")
    sleep(1)
    print("Please select a class: ")
    print("Classes:", classes_list, sep="\n")

    chosen_class = ""
    while chosen_class not in classes_list:
        try:
            chosen_class = input("> ").capitalize()
            sleep(1)
            if chosen_class not in classes_list:
                print("Sorry, that is not a valid class. Please try again.\n")
                sleep(1)
                raise ValueError
            break
        except ValueError:
            pass
    player = eval(f"{chosen_class}('{name}')")

# ------------------ Stats ------------------ #

def upgrade_stats(player):
    print("Please select a stat to upgrade: ")
    print("1. Health")
    print("2. Attack")
    print("3. Defense")
    print("4. Magic")
    print("5. Exit")

    user_input = input("> ")
    sleep(1)
    if user_input == "1":
        player.health += 10
        player.points -= 1
        print("You have upgraded your health by 10.")
        print("You have", player.points, "points left.")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "2":
        player.attack += 5
        player.points -= 1
        print("You have upgraded your attack by 5.")
        print("You have", player.points, "points left.")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "3":
        player.defense += 5
        player.points -= 1
        print("You have upgraded your defense by 5.")
        print("You have", player.points, "points left.")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "4":
        player.magic += 5
        player.points -= 1
        print("You have upgraded your magic by 5.")
        print("You have", player.points, "points left.")
        sleep(1)
        upgrade_stats(player)
    elif user_input == "5":
        print("You have exited the upgrade menu.")
        sleep(1)
        main_menu()
    else:
        print("Sorry, that is not a valid option. Please try again.\n")
        sleep(1)
        upgrade_stats(player)

# ------------------ Start Game ------------------ #


def start_game():
    character_selection()


# ------------------ Main Menu ------------------ #

# This is the main menu that the player will see when they start the game.
def main_menu():
    print("--------------------------------")
    print("Welcome To Melon Man's Text RPG!")
    print("--------------------------------")
    print("Please select an option:")
    print("1. Start game")
    print("2. Exit game")
    # print("3. View credits")
    # print("4. View help")
    # print("5. View high scores")
    # print("6. View settings")
    # print("7. View achievements")
    # print("8. View stats")
    # print("9. View inventory")
    # print("10. View quests")
    # The above are placeholders currently

    user_input = input("> ")
    sleep(1)
    if user_input == "1":
        start_game()
        pass
    elif user_input == "2":
        exit()
    # elif user_input == "3":
    #     view_credits()
    # elif user_input == "4":
    #     view_help()
    # elif user_input == "5":
    #     view_high_scores()
    # elif user_input == "6":
    #     view_settings()
    # elif user_input == "7":
    #     view_achievements()
    # elif user_input == "8":
    #     view_stats()
    # elif user_input == "9":
    #     view_inventory()
    # elif user_input == "10":
    #     view_quests()
    else:
        print("Sorry, that is not a valid option. Please try again.\n")
        sleep(1)
        main_menu()


#main_menu()

map = Map(5, 5)
print(map.create_detailed_map())
