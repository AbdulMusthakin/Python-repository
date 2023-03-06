import random
from time import sleep
import os
import pickle


class Quiz:
    def __init__(
        self,
        questions,
        score=0,
        randomize_questions=False,
        attempts=3,
    ):
        self.randomize_questions = randomize_questions
        if self.randomize_questions:
            shuffled_questions = questions[:]
            random.shuffle(shuffled_questions)
            self.questions = shuffled_questions
        else:
            self.questions = questions

        self.score = score
        self.attempts = attempts

    def run_quiz(self):
        os.system("cls")
        for i, j in enumerate(self.questions):

            print(
                "------------------------------------------------------------------------------------------"
            )
            print(f"Question {i + 1}: {j.question}")
            print(
                "------------------------------------------------------------------------------------------"
            )

            user_answer = ""
            for k in range(self.attempts, 0, -1):
                user_answer = input("Your answer: ").title()
                print()
                if j.check_answer(user_answer, k):
                    self.score += 1
                    break
            else:
                print("You ran out of attempts.")
        sleep(1)
        print("=============================================")


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer(self, user_answer, attempts):
        if user_answer == self.answer:
            print("You got it right!")
            return True
        else:
            print("That's wrong.")
            print(f"The correct answer was: {self.answer}")
            sleep(1)

            print(f"You have {attempts - 1} attempts left")
            return False

    def __str__(self) -> str:
        return f"{self.question} {self.answer}"


class Player:
    def __init__(self, name, personal_leaderboard={}):
        self.name = name
        self.personal_leaderboard = personal_leaderboard

    def __str__(self) -> str:
        return f"{self.name} {self.personal_leaderboard}"


class Leaderboard:
    def __init__(self, players=[]):
        self.players = players

    def get_player(self, name):

        for i in self.players:
            if i.name == name:
                return self.players.index(i)

    def __str__(self) -> str:
        return f"{self.players}"


leaderboard = Leaderboard()

hardware_questions: list[Question] = [
    Question(
        "What does the R in ROM stand for?",
        "Read",
    ),
    Question(
        "What does ALU stand for?",
        "Arithmetic Logic Unit",
    ),
    Question(
        "What does the R in RAM stand for?",
        "Random",
    ),
    Question(
        "Which type of main memory storage is closest to the CPU?",
        "Registers",
    ),
    Question(
        "What is the fastest type of Cache?",
        "L1",
    ),
    Question(
        "What is the main circuit board of computers?",
        "Motherboard",
    ),
    Question(
        "What's the architecture which many general purpose computers are based on?",
        "Von Neumann Architecture",
    ),
    Question(
        "What word describes RAM losing it's data when the computer is powered off?",
        "Volatile",
    ),
    Question(
        "What part of the computer is the BIOS stored?",
        "Rom",
    ),
    Question(
        "True or False - Optical storage devices have no moving parts.",
        "False",
    ),
    Question(
        "How much 20MB files can fit into a 4TB drive?(Don't include commas)",
        "200000",
    ),
    Question(
        "True or False - A CPU with 4x cores wont always have 4x performance.", "True"
    ),
    Question(
        "what type of device is a mouse?(Input/Output)",
        "Input",
    ),
    Question(
        "Which would a mobile phone use, RISC or CISC.",
        "Risc",
    ),
    Question(
        "What hardware component is used to produce high-quality images (abbreviation)?",
        "Gpu",
    ),
]

network_questions: list[Question] = [
    Question(
        "What represents the connections in a network?",
        "Edges",
    ),
    Question(
        "What represents the devices in a network?",
        "Nodes",
    ),
    Question(
        "Can devices in peer-to-peer networks act as the client and server (Yes/No)?",
        "Yes",
    ),
    Question(
        "What is the most common network topology?",
        "Mesh",
    ),
    Question(
        "What is the top layer of the TCP/IP model?",
        "Application Layer",
    ),
    Question(
        "What is the cheapest network topology?",
        "Bus",
    ),
    Question(
        "Which of these is a Link Layer Protcol: UDP, WIFI, IP, TCP, IMAP",
        "Wifi",
    ),
    Question(
        "What type of tranmission media has the highest bandwith?",
        "Fibre Optic",
    ),
    Question(
        "What word is the delay between a signal being sent and received?",
        "Latency",
    ),
    Question(
        "What's the type of computer network used over large areas (abbreviation)?",
        "Wan",
    ),
]


all_quizzes = {
    1: [hardware_questions, "Hardware"],
    2: [network_questions, "Networks"],
}


def view_leaderboard():

    with open("GCSE Computer Science/Miscellaneous/Quiz/leaderboard.txt", "rb") as f:
        leaderboard = pickle.load(f)

    print(f"Leaderboard:")
    for i in leaderboard.players:
        print(f"Name: {i.name}, {i.personal_leaderboard}")
    print()
    hardware_max_score = 0
    hardware_max_player = ""
    for i in leaderboard.players:
        try:
            if i.personal_leaderboard["Hardware"][0] > hardware_max_score:
                hardware_max_score = i.personal_leaderboard["Hardware"][0]
                hardware_max_player = i.name
        except KeyError:
            pass
    print("Hardware:")
    print(f"Top player: {hardware_max_player} with a score of {hardware_max_score}")

    sleep(1)
    networks_max_score = 0
    networks_max_player = ""
    for i in leaderboard.players:
        try:
            if i.personal_leaderboard["Networks"][0] > networks_max_score:
                networks_max_score = i.personal_leaderboard["Networks"][0]
                networks_max_player = i.name
        except KeyError:
            pass

    print()
    print("Networks:")

    print(f"Top player: {networks_max_player} with a score of {networks_max_score}")

    print()
    sleep(1)


def store_score(score, quiz):

    try:
        with open(
            "GCSE Computer Science/Miscellaneous/Quiz/leaderboard.txt", "rb"
        ) as f:
            leaderboard = pickle.load(f)
    except EOFError:
        leaderboard = Leaderboard()

    played_before = input("Have you played before? (Y/N) ").lower()
    if played_before == "y":
        name = input("Please enter your name: ").lower()
        player_index = leaderboard.get_player(name)
        leaderboard.players[player_index].personal_leaderboard[quiz] = [score]

    else:
        name = input("Please enter your name: ").lower()

        player = Player(name)
        player.personal_leaderboard[quiz] = [score]

        print(player.personal_leaderboard)
        leaderboard.players.append(player)

    with open("GCSE Computer Science/Miscellaneous/Quiz/leaderboard.txt", "wb") as f:
        pickle.dump(leaderboard, f)


def quiz_selection():
    print("Welcome to Quiz Selection")
    print("Which set of questions would you like to do?")
    print("1. Hardware")
    print("2. Networks")

    user_input = input("> ")
    sleep(1)

    if user_input not in ["1", "2"]:
        print("Please enter a valid number.")
        return quiz_selection()

    print("Do you want to Shuffle the questions? (Y/N)")

    while True:
        try:
            shuffle_input = input("> ").lower()
            sleep(1)
            break
        except ValueError:
            print("Please enter a valid input.")
            sleep(1)

    if shuffle_input == "y":
        quiz = Quiz(all_quizzes[int(user_input)][0], randomize_questions=True)
    else:
        quiz = Quiz(all_quizzes[int(user_input)][0])

    quiz.run_quiz()

    sleep(1)

    print(f"You got {quiz.score} out of {len(quiz.questions)} correct.")

    store_score(quiz.score, all_quizzes[int(user_input)][1])

    print("Returning to main menu...")
    sleep(1)


def intro():
    """Just the introduction to the revision quiz code."""
    print(
        """
    Hello, Welcome to this Computer Science Revision Quiz!
    You can test yourself against two different topics, hardware and networks.
    After selecting a topic to do, you will be asked a series of questions and be given
    a few attempts to answer them. Your score will increase every question you get right
    and you'll be told your result after completing the quiz.
    """
    )
    sleep(5)
    print(
        "There isn't much else to this, so now you'll be directerd to the main menu. \n"
    )
    sleep(1)
    main()


def main(intro_has_ran=True):
    """The main part of the code where the player can go the selection place,
    leaderboard, or decide to the quit the program.
    """

    if intro_has_ran is False:
        intro()  # Only runs once

    print(
        "Main Menu - Press 1 to see quiz selection. Press 2 to see leaderboard. Press 3 to quit. \n"
    )
    try:
        user_input = input("> ").lower()
        sleep(1)
        if user_input == "1":
            quiz_selection()
            main()
        elif user_input == "2":
            view_leaderboard()
            main()
        elif (
            user_input == "3"
        ):  # If 3 is entered then no ValueError happens and the function ends.
            exit()
        else:
            raise ValueError
    except ValueError:
        print("You have entered an invalid option. Try Again: \n")
        sleep(1)
        main()  # We don't have to make a while loop hear since the code would end now so we just


if __name__ == "__main__":
    main(intro_has_ran=False)
