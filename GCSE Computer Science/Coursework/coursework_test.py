import unittest
from unittest.mock import patch
import python_coursework_home as pch
import sys
import os


class TestCoursework(unittest.TestCase):
    @patch("builtins.input")
    def test_chosen_message(self, mocked_input):
        mocked_input.side_effect = ["y", "Bob", "Test"]

        self.assertEqual(pch.choose_personalised_message(), "Bob. Test")

    @patch("builtins.input")
    def test_choose_tin_contents(self, mocked_input):
        mocked_input.side_effect = ["", "1", 500, "y", "2", 400, "y", "3", 100, "y"]

        self.assertEqual(
            pch.choose_tin_contents(),
            {"Caramel Twist": 500, "Orange Crush": 400, "Chocolate Bar": 100},
        )


class SaveTests:
    def __init__(self):
        self.location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        self.log_file = os.path.join(self.location, "test_log.txt")
        self.results = os.path.join(self.location, "test_results.txt")

    def log_tests(self):

        with open(self.log_file, "w") as f:
            suit = unittest.TestLoader().loadTestsFromTestCase(TestCoursework)
            unittest.TextTestRunner(stream=f, verbosity=2, buffer=True).run(suit)

    def export_test_results(self):

        with open(self.results, "r+") as f:
            lines = f.readlines()
            lines = [line.strip() if line.strip() != "" else line for line in lines]
            print(lines)
            last_line = lines[-1]
            test_num = str(int(last_line.split(" ")[1][:-1]) + 1)

            with open(self.log_file, "r") as g:
                f.write("~" * 50 + "\n")
                f.write(g.read())
                f.write("~" * 50 + "\n\n")
                f.write("Test " + test_num + ")\n")


if __name__ == "__main__":

    st = SaveTests()
    st.log_tests()
    st.export_test_results()
