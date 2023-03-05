import unittest
from unittest.mock import patch
import python_coursework_home as pch


class CourseworkTest(unittest.TestCase):
    @patch("builtins.input")
    def test_chosen_message(self, mocked_input):
        mocked_input.side_effect = ["y", "Bob", "Test"]

        self.assertEqual(pch.choose_personalised_message(), "Bob. Test")


if __name__ == "__main__":
    unittest.main()
