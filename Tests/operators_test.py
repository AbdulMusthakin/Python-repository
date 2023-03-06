import math
import pytest


def addition(a, b):
    return a + b


def subtraction(a, b):
    return a - b


def multiplication(a, b):
    return a * b


def division(a, b):
    return a / b


def test_addition():
    assert addition(1, 2) == 3
    assert addition(1, 3) == 4


if __name__ == "__main__":
    pytest.main()
