import unittest
from unittest.mock import patch
import python_coursework_home as pch


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


if __name__ == "__main__":
    unittest.main()
