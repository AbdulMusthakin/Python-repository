import pytest


def return_negative_number():
    num = int(input("Enter a positive number (not 0): "))
    if num <= 0:
        raise ValueError("You can only enter a positive number")

    return -num


def test_negative_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: -1)
    with pytest.raises(ValueError):
        return_negative_number()


def test_zero(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 0)
    with pytest.raises(ValueError):
        return_negative_number()


def test_positive_number(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert return_negative_number() == -1
