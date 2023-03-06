import pytest


def add_ice_cream():
    ice_creams = {"chocolate": 100, "vanilla": 100}

    ice_cream_to_add = input("What ice cream would you like to add? ")

    amount_to_add = int(input("How much grams would you like to add "))

    ice_creams[ice_cream_to_add] += amount_to_add

    return ice_creams


def test_add_ice_cream(monkeypatch):

    inputs = iter(["chocolate", "200"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert add_ice_cream() == {"chocolate": 300, "vanilla": 100}
