import json
import random


def rules():
    print("Welcome to Wordle!")
    print("The aim of the game is to guess the word in 5 guesses.")
    print("The word is a 5 letter word.")
    print("You will be given feedback on your guesses.")
    print(
        "If a letter is correct and in the correct position, it will be marked green."
    )
    print("If a letter is correct but in the wrong position, it will be marked yellow.")
    print("If a letter is incorrect, it will be marked red.")
    print("Good luck!")


def print_grid(grid):
    for row in grid:
        for letter in row:
            print(letter, end=" ")
        print()


def main():
    with open(
        "GCSE Computer Science/Miscellaneous/Wordle/5_letter_words.json", "r"
    ) as f:
        data_dict_list = json.load(f)
        data_list: list[str] = [data_dict["word"] for data_dict in data_dict_list]

    rules()

    guesses_grid = [
        [],
        [],
        [],
        [],
        [],
    ]

    list_of_chosen_words = []

    correct_word = random.choice(data_list)

    for i in range(5):
        print("Choose a word:")

        chosen_word = ""
        valid = False
        while not valid:
            try:
                chosen_word = input("> ").lower()

                if chosen_word not in data_list:
                    print("Please enter a valid 5-letter word.")
                    raise ValueError

                if chosen_word in list_of_chosen_words:
                    print("You have already chosen that word.")
                    raise ValueError

                valid = True
            except ValueError:
                pass

            list_of_chosen_words.append(chosen_word)

        # Go through list and change item to corresponding letter of chosen word
        for letter in chosen_word:
            if letter in correct_word:
                if chosen_word.index(letter) == correct_word.index(letter):
                    guesses_grid[i].append("\033[1;32;1m" + letter + "\033[0m")
                else:
                    guesses_grid[i].append("\033[1;33;1m" + letter + "\033[0m")
            else:
                guesses_grid[i].append("\033[1;31;1m" + letter + "\033[0m")

        print_grid(guesses_grid)

        if chosen_word == correct_word:
            print("\nCongratulations! You guessed the word!")
            break
    else:
        print("\nYou have run out of guesses.")
        print("The correct word was", correct_word)


if __name__ == "__main__":
    main()
