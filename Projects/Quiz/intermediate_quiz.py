"""This quiz will be similar to the previous one but we will use a bit more advance techniques in Python when coding it.
"""
import random


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


countries_questions: list[Question] = [
    Question("What is the capital of France?", "Paris"),
    Question("What is the capital of Germany?", "Berlin"),
    Question("What is the capital of Spain?", "Madrid"),
    Question("What is the capital of Italy?", "Rome"),
    Question("What is the capital of Poland?", "Warsaw"),
    Question("What is the capital of Portugal?", "Lisbon"),
    Question("What is the capital of Greece?", "Athens"),
    Question("What is the capital of Sweden?", "Stockholm"),
    Question("What is the capital of Norway?", "Oslo"),
]

countries_quiz = Quiz(questions=countries_questions, score=0)  # Create a quiz object

countries_quiz.run_quiz()  # Run the quiz
print(f"Score: {countries_quiz.score}")
