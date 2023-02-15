# This is a text based rpg game that I am working on. It is a work in progress.

# ------------------ Importing Modules ------------------ #

import random
from time import sleep
import os
import pickle



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
    

class Zone(Map):
    def __init__(self, name, description="", is_player_here=False, map=Map(5, 5)):
        self.height = map.height
        self.name = name
        self.description = description
        self.is_player_here = is_player_here

    def place_player(self):
        self.is_player_here = True

    def remove_player(self):
        self.is_player_here = False

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"

    def check_border(self):
        loaded_zones = [self.name]
        at_top_border, at_bottom_border, at_left_border, at_right_border = False, False, False, False
        split_name = [x for x in self.name]

        
        if split_name[1] == "1":
            at_top_border = True
        else:
            loaded_zones.append(split_name[0] + str(int(split_name[1]) - 1))
        
        if split_name[1] == str(self.height): 
            at_bottom_border = True
        else:
            loaded_zones.append(split_name[0] + str(int(split_name[1]) + 1))
        
        if split_name[0] == "A":
            at_left_border = True
        else:
            loaded_zones.append(chr(ord(split_name[0]) - 1) + split_name[1])
        
        if split_name[0] == chr(self.height + 64):
            at_right_border = True
        else:
            loaded_zones.append(chr(ord(split_name[0]) + 1) + split_name[1])        


        return at_top_border, at_bottom_border, at_left_border, at_right_border, loaded_zones

    def up(self, game_data):
        if game_data.tb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((split_name[0] + str(int(split_name[1]) - 1)), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further up.")
            sleep(1)
            move(game_data)
    
    def down(self, game_data):
        if game_data.bb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((split_name[0] + str(int(split_name[1]) + 1)), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further down.")
            sleep(1)
            move(game_data)

    def left(self, game_data):
        if game_data.lb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((chr(ord(split_name[0]) - 1) + split_name[1]), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further left.")
            sleep(1)
            move(game_data)
    
    def right(self, game_data):
        if game_data.rb == False:
            self.remove_player()
            split_name = [x for x in self.name]
            new_zone = Zone((chr(ord(split_name[0]) + 1) + split_name[1]), description=create_description())
            new_zone.place_player()
        else:
            print("You can't go any further right.")
            sleep(1)
            move(game_data)
            
        
# ------------------ Zone Descriptions ------------------ #

# This function will create a description for the zone.
# It will use a list of adjectives, nouns, and verbs to create a description.
# For example, "This dark room smells clean."

def create_description():
    adjectives = ["dark", "mighty", "cold", "warm", "wet", "dry", "quiet", "loud", "smelly", "clean", "dirty", "empty", "full", "bright", "giant", "tiny", "unusual", "strange", "odd", "weird"]
    nouns = ["room", "tower", "ruins", "bathroom", "bedroom", "hut", "fort", "basement", "attic", "garage", "closet", "office", "library", "garden", "yard", "field", "balcony", "staircase", "hallway", "hallway"]
    verbs = ["smells", "feels", "looks", "sounds", "tastes", "seems", "feels", "looks", "sounds", "tastes", "smells", "feels", "looks", "sounds", "appears", "smells", "feels", "looks", "sounds", "tastes"]
    
    return f"This {random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)} {random.choice(adjectives)}."

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

    return player

# ------------------ Stats ------------------ #

def upgrade_stats(player):
    if player.points == 0:
        print("You have no points left.")
        sleep(1)
        return player
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
    else:
        print("Sorry, that is not a valid option. Please try again.\n")
        sleep(1)
        upgrade_stats(player)

    return player

# ------------------ Interact ------------------ #

def interact(game_data):
    print("What do you want to do?")
    print("1. Move")
    print("2. View stats")
    print("3. Upgrade stats")
    print("4. Save game")
    print("5. Exit game")

    user_input = input("> ")
    sleep(1)
    if user_input == "1":
        move(game_data)
        sleep(1)
        interact(game_data)
    elif user_input == "2":
        print(game_data.player)
        sleep(1)
        interact(game_data)
    elif user_input == "3":
        game_data.player = upgrade_stats(game_data.player)
        interact(game_data)
    elif user_input == "4":
        game_data.save_menu()
        interact(game_data)
    elif user_input == "5":
        print("Do you want to save your game before exiting?(y/n)")
        user_input2 = input("> ").lower()
        if user_input2 == "y":
            game_data.save_menu()
        elif user_input2 == "n":
            print("You have returned to main menu.")
            game_data.game_is_running = False
            sleep(1)
            main_menu(game_data)
        else:
            print("Sorry, that is not a valid option. Please try again.\n")
            sleep(1)
            interact(game_data)
    else:
        print("Sorry, that is not a valid option. Please try again.\n")
        sleep(1)
        interact(game_data)

# ------------------ Move ------------------ #

def move(game_data):
    print("Please select a direction to move in:")
    print("1. Up")
    print("2. Down")
    print("3. Left")
    print("4. Right")

    user_input = input("> ")
    sleep(1)
    if user_input == "1":
        game_data.zone.up(game_data)
    elif user_input == "2":
        game_data.zone.down(game_data)
    elif user_input == "3":
        game_data.zone.left(game_data)
    elif user_input == "4":
        game_data.zone.right(game_data)
    else:
        print("Sorry, that is not a valid option. Please pick the number associated with the direction.\n")
        sleep(1)
        return move(game_data)


# ------------------ Start Game ------------------ #


def start_game():
    player = character_selection()

    a1 = Zone("A1", is_player_here=True, description = "This is the starting zone, your adventure awaits.")
    tb, bb, lb, rb, loaded_zones = a1.check_border()
    game_data = GameData(player, a1, tb, bb, lb, rb, loaded_zones, True)
    print(a1)
    interact(game_data)


# ------------------ View Credits ------------------ #

def view_credits(game_data):
    print("--------------------------------")
    print("           Credits:"             )
    print("    Created by: Melon Man"       )
    print("    Designed by: Melon Man"      )
    print("   Illustrated by: Melon Man"    )
    print("   Hope you enjoyed the game!"   )
    print("--------------------------------")
    sleep(5)
    main_menu(game_data)



# ------------------ Save Data ------------------ #

class GameData:
    def __init__(self, player, zone, tb, bb, lb, rb, loaded_zones, game_is_running):
        self.player = player
        self.zone = zone
        self.tb = tb
        self.bb = bb
        self.lb = lb
        self.rb = rb
        self.loaded_zones = loaded_zones
        self.game_is_running = game_is_running

    def save_menu(self):
        print("Do you want to import or export save data?")
        print("1. Import")
        print("2. Export")
        print("3. Exit to Main Menu")
        print("4. Exit to Game")

        user_input = input("> ")
        sleep(1)

        if user_input == "1":
            self.import_data()
        elif user_input == "2":
            self.export_data()
        elif user_input == "3":
            if self.game_is_running == True:
                print("Do you not want to return back to the game? You may lose data. (y/n).")
                user_input2 = input("> ").lower()
                sleep(1)

                if user_input2 == "y":
                    print("Returning back to save menu.")
                    sleep(1)
                    self.game_is_running = False
                    self.save_menu()            
                elif user_input2 == "n":
                    print("Returning back to game.")
                    sleep(1)
                    return self
                else:
                    print("Sorry, that is not a valid option. Please try again.\n")
                    sleep(1)
                    self.save_menu()
            else:
                print("You have exited the save menu.")
                sleep(1)
                main_menu(self)
        
        elif user_input == "4":
            if self.game_is_running == True:
                print("You have exited the save menu.")
                sleep(1)
                return self
            else:
                print("You are not currently running a game. Exiting to main menu.")
                sleep(1)
                main_menu(self)
        else:
            print("Sorry, that is not a valid option. Please try again.\n")
            sleep(1)
            self.save_menu()

    def export_data(self):
        print("Please enter the name of the save file you want to export to.(1, 2 or 3) Or enter 4 to exit.")
        user_input = input("> ")
        sleep(1)

        if int(user_input) in range(1, 4):
            print("Are you sure, this will overwrite the save file. (y/n)")
            user_input2 = input("> ").lower()
            sleep(1)

            if user_input2 == "y":
                with open(fr"Projects\Text RPG\Save Files\save{user_input}.txt", "wb") as file:
                    pickle.dump(self, file)
                    print(f"You have exported your save data to save{user_input}.txt")
                    sleep(1)
                self.save_menu()
            elif user_input2 == "n":
                print("You have exited the export menu.")
                sleep(1)
                self.save_menu()
            else:
                print("Sorry, that is not a valid option. Please try again.\n")
                sleep(1)
                self.export_data()
        
        elif user_input == "4":
            print("You have exited the export menu.")
            sleep(1)
            self.save_menu()
        else:
            print("Sorry, that is not a valid option. Please try again.\n")
            sleep(1)
            self.export_data()

    def import_data(self):
        print("Please enter the name of the save file you want to import from.(1, 2 or 3) Or enter 4 to exit.")
        user_input = input("> ")
        sleep(1)

        if int(user_input) in range(1, 4):
            print("Are you sure, this will overwrite your current save. (y/n)")
            user_input2 = input("> ").lower()
            sleep(1)

            if user_input2 == "y":
                with open(fr"Projects\Text RPG\Save Files\save{user_input}.txt", "rb") as file:
                    self = pickle.load(file)
                    print(f"You have imported save{user_input}.txt")
                    sleep(1)
                self.save_menu()
            elif user_input2 == "n":
                print("You have exited the import menu.")
                sleep(1)
                self.save_menu()
            else:
                print("Sorry, that is not a valid option. Please try again.\n")
                sleep(1)
                self.import_data()
        elif user_input == "4":
            print("You have exited the import menu.")
            sleep(1)
            self.save_menu()
        else:
            print("Sorry, that is not a valid option. Please try again.\n")
            sleep(1)
            self.import_data()


    def __str__(self):
        return "Player: " + str(self.player) + ""



# ------------------ Main Menu ------------------ #

# This is the main menu that the game_data will see when they start the game.
def main_menu(game_data):
    print("--------------------------------")
    print("Welcome To Melon Man's Text RPG!")
    print("--------------------------------")
    print("Please select an option:")
    print("1. Start game")
    print("2. Exit game")
    print("3. View credits")
    print("4. Open save menu")
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
    elif user_input == "3":
        view_credits(game_data)
    elif user_input == "4":
        game_data.save_menu()
    # elif user_input == "5":
    #     view_help()
    # elif user_input == "6":
    #     view_high_scores()
    # elif user_input == "7":
    #     view_settings()
    # elif user_input == "8":
    #     view_achievements()
    # elif user_input == "9":
    #     view_stats()
    # elif user_input == "10":
    #     view_inventory()
    # elif user_input == "11":
    #     view_quests()
    else:
        print("Sorry, that is not a valid option. Please try again.\n")
        sleep(1)
        main_menu(game_data)


main_menu(game_data=GameData(player=Warrior("Placeholder"), zone="A1", tb=True, bb=False, lb=True, rb=False, loaded_zones=[], game_is_running=False))

#map = Map(26, 26)
# for i in map.create_detailed_map().values():
#     for j in i:
#         print(str(j).strip("[]"))
# a1 = Zone("A1")
# a1.check_border()
# a1 = Zone("A1")
# tb, bb, lb, rb, loaded_zones = a1.check_border()
# print(tb, bb, lb, rb, loaded_zones)