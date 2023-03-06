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


def exponentiation(a, b):
    return a**b


def square_root(a):
    return math.sqrt(a)


def log(a):
    return math.log(a)


def test_addition():
    assert addition(1, 2) == 3
    assert addition(1, 3) == 4


def test_subtraction():
    assert subtraction(1, 2) == -1
    assert subtraction(1, 3) == -2


def test_multiplication():
    assert multiplication(1, 2) == 2
    assert multiplication(4, 3) == 12


def test_division():
    assert division(1, 2) == 0.5
    assert division(4, 2) == 2


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        division(1, 0)
    with pytest.raises(ZeroDivisionError):
        division(4, 0)


def test_exponentiation():
    assert exponentiation(2, 2) == 4
    assert exponentiation(4, 3) == 64


def test_square_root():
    assert square_root(4) == 2
    assert square_root(9) == 3


def test_log():
    assert log(1) == 0
    assert log(math.e) == 1
