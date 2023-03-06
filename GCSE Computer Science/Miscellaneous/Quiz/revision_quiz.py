from time import sleep
import random


INTRO_HAS_RAN = False
NAME_CHOSEN = False
# These two variables above are to make it so the introduction and name selection only happen once.

leaderboard = {
    # A made-up leaderboard that the user can add their name to after completing a quiz
    "Bob": 1,
    "Tim": 4,
    "Jim": 0,
    "Bartholamew": 10,
}

hardware_questions = {
    # A nested dictionary. A dictionary that contains a dictionary.
    # Here, it's an index of each question and a dictionary containing a question and answer.
    1: {"question": "What does the R in ROM stand for?", "answer": "Read"},
    2: {"question": "What does ALU stand for?", "answer": "Arithmetic Logic Unit"},
    3: {"question": "What does the R in RAM stand for?", "answer": "Random"},
    4: {
        "question": "Which type of main memory storage is closest to the CPU?",
        "answer": "Registers",
    },
    5: {"question": "What is the fastest type of Cache?", "answer": "L1"},
    6: {
        "question": "What is the main circuit board of computers?",
        "answer": "Motherboard",
    },
    7: {
        "question": "What's the architecture which many general purpose computers are based on?",
        "answer": "Von Neumann Architecture",
    },
    8: {
        "question": "What word describes RAM losing it's data when the computer is powered off?",
        "answer": "Volatile",
    },
    9: {"question": "What part of the computer is the BIOS stored?", "answer": "Rom"},
    10: {
        "question": "True or False - Optical storage devices have no moving parts.",
        "answer": "False",
    },
    11: {
        "question": "How much 20MB files can fit into a 4TB drive?(Don't include commas)",
        "answer": "200000",
    },
    12: {
        "question": "True or False - A CPU with 4x cores wont always have 4x performance.",
        "answer": "True",
    },
    13: {
        "question": "what type of device is a mouse?(Input/Output)",
        "answer": "Input",
    },
    14: {"question": "Which would a mobile phone use, RISC or CISC.", "answer": "Risc"},
    15: {
        "question": "What hardware component is used to produce high-quality images (abbreviation)?",
        "answer": "Gpu",
    },
}

network_questions = {
    1: {"question": "What represents the connections in a network?", "answer": "Edges"},
    2: {"question": "What represents the devices in a network?", "answer": "Nodes"},
    3: {
        "question": "Can devices in peer-to-peer networks act as the client and server (Yes/No)?",
        "answer": "Yes",
    },
    4: {"question": "What is the most common network topology?", "answer": "Mesh"},
    5: {
        "question": "What is the top layer of the TCP/IP model?",
        "answer": "Application Layer",
    },
    6: {"question": "What is the cheapest network topology?", "answer": "Bus"},
    7: {
        "question": "Which of these is a Link Layer Protcol: UDP, WIFI, IP, TCP, IMAP",
        "answer": "Wifi",
    },
    8: {
        "question": "What type of tranmission media has the highest bandwith?",
        "answer": "Fibre Optic",
    },
    9: {
        "question": "What word is the delay between a signal being sent and received?",
        "answer": "Latency",
    },
    10: {
        "question": "What's the type of computer network used over large areas (abbreviation)?",
        "answer": "Wan",
    },
}

all_quizzes = {
    # This is more efficient than having indivisual if statements, especially with more quizzes
    1: hardware_questions,
    2: network_questions,
}


def quiz_selection(score):
    """Lets the user select which quiz they want to do,
    more efficient than indivisual subroutines especially
    with a larger amount of topics.

    Args:
        score (int): The players score earnt by getting questions right.
    """
    print(
        "Welcome to Quiz Selection",
        "Press 1 to attempt Hardware Quiz",
        "Press 2 to attempt Network Quiz",
    )
    try:
        user_input = int(input())
        score = quiz(all_quizzes[user_input], score)
    except KeyError:
        # An error that would happen if python tries to find a dictionary key that doesn't exist.
        print("Invalid. Try Again: ")
        sleep(1)
    sleep(1)
    print(f"Finished! Your score is {score}.")
    global NAME_CHOSEN
    while True:
        try:
            name = ""
            if NAME_CHOSEN is False:  # Only runs once.
                name = input(
                    "Your score will be added to the leaderboard.\nEnter your name: "
                )
                NAME_CHOSEN = True
            leaderboard.update({name.capitalize(): score})
            # Updates the value of a key if it already exists or adds a new one if it doesn't.
            if name == "":
                raise ValueError
            break
        except ValueError:
            print("Please Enter Something")
            sleep(1)
    sleep(1)
    print("You will now be sent to the Main Menu:")


def check_answer(quiz_arg, question_arg, answer_arg, attempts_arg):
    """This function checks whether the user has entered in the correct
    answer to the current question and then returns a boolean value
    depending on that.

    Args:
        quiz_arg (dict): The dictionary containing the questions of the current quiz topic.
        question_arg (int): The current question number that is being attempted.
        answer_arg (str): The answer provided by the user.
        attempts_arg (int): The current amount of attempts the user has for the current question.

    Returns:
        bool: Boolean value depending on whether the user got the question right or wrong
    """
    if quiz_arg[question_arg]["answer"] == answer_arg.title():
        # The above line takes the dictionary associated with a key in the quiz (dict outside nested dict),
        # and the value of 'answer' inside of that dictionary.
        print("Correct!")
        return True
    # Everything in this function below this will only run if the if statement above is false,
    # because otherwise the return statement runs and ends the function. So I dont need to use else.
    print(f"Incorrect! You have {attempts_arg - 1} attempts left.")
    # Above uses - 1 because one attempt will be lost afterwards since user got question incorrect.
    if attempts_arg == 1:  # not 0 because user would have lost an attempt.
        print("You ran out of tries")
        print(f"The answer was '{quiz_arg[question_arg]['answer']}'")
    return False


def quiz(questions_dict, score):
    """The actual revision quiz. Goes through a dictionary of questions
    in a random order and lets the user enter in an answer for them,
    given a limited amount of attempts

    Args:
        questions_dict (dict): The dictionary containing the questions of the current topic.
        score (int): The score of the user earnt by getting questions right.

    Returns:
        int: The score of the user after finishing the quiz.
    """
    questions_dict_list = list(questions_dict.items())
    # Could do this in two lines but less readble.
    # First, we get a view object of the dictionary with .items() and create a list with it.
    random.shuffle(questions_dict_list)
    # Then we shuffle that list with random.shuffle()
    questions_dict = dict(questions_dict_list)
    # Lastly, we turn this list back into a dictionary and assign it to the original dictionary.
    # Wouldn't it be neat if there was just a method that shuffled dictionaries for you?
    for key, questions in questions_dict.items():
        # The key here numbers all the questions which is useful for the check_answer() function.
        if "True" in questions["question"] or "Yes" in questions["question"]:
            attempts = 1
        # This checks if the question is a True and False one,
        # since you don't want to give multiple attempts for that.
        else:
            attempts = 3
        while attempts > 0:
            print(questions["question"])
            # This is a part of the quiz that is different from my original quiz I did.
            # Previously, I did quiz[question]['question'] and looped through the quiz normally.
            # Now I have used .items() to loop through it and make the code cleaner.
            answer = input("Enter Answer: ")
            check = check_answer(questions_dict, key, answer, attempts)
            if check:
                score += 1
                break
            # Since you don't need to go through the question again after getting it right.
            attempts -= 1
    return score


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


def main():
    """The main part of the code where the player can go the selection place,
    leaderboard, or decide to the quit the program.
    """
    score = 0
    global INTRO_HAS_RAN
    if INTRO_HAS_RAN is False:
        INTRO_HAS_RAN = True
        intro()  # Only runs once
    try:
        user_input = input(
            "Main Menu - Press 1 to see quiz selection. Press 2 to see leaderboard. \
Press 3 to quit. \n"
        )
        sleep(1)
        if user_input == "1":
            quiz_selection(score)
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
    main()
