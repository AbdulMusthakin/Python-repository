import random
from time import sleep
import pickle


class Quiz:
    def __init__(
        self,
        questions,
        score=0,
        randomize_questions=False,
    ):
        self.randomize_questions = randomize_questions
        if self.randomize_questions:
            shuffled_questions = questions[:]
            random.shuffle(shuffled_questions)
            self.questions = shuffled_questions
        else:
            self.questions = questions

        self.score = score

    def run_quiz(self):
        for i, j in enumerate(self.questions):

            print(f"Question {i + 1}: {j.question}")

            user_answer = input("Your answer: ").title()

            self.score = j.check_answer(user_answer, self.score)


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer(self, user_answer, score):
        if user_answer == self.answer:
            print("You got it right!")
            score += 1
        else:
            print("That's wrong.")
            print(f"The correct answer was: {self.answer}")

        return score

    def __str__(self) -> str:
        return f"{self.question} {self.answer}"


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
    1: hardware_questions,
    2: network_questions,
}


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
        quiz = Quiz(all_quizzes[int(user_input)], randomize_questions=True)
    else:
        quiz = Quiz(all_quizzes[int(user_input)])

    quiz.run_quiz()


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
    score = 0

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
        elif user_input == "2":
            print(leaderboard)
            sleep(1)
            print("You can add/update your name on this leaderboard.")
            sleep(1)
            print("Returning to Main Menu:")
            sleep(1)
            main()
        elif (
            user_input == "3"
        ):  # If 3 is entered then no ValueError happens and the function ends.
            pass
        else:
            raise ValueError
    except ValueError:
        print("You have entered an invalid option. Try Again: \n")
        sleep(1)
        main()  # We don't have to make a while loop hear since the code would end now so we just
        # call the main() function again which does the same thing as while loop but cleaner.


if __name__ == "__main__":
    main(intro_has_ran=False)
