import pytest


def add_ice_cream():
    ice_creams = {"chocolate": 100, "vanilla": 100}

    ice_cream_to_add = input("What ice cream would you like to add? ")

    ice_creams[ice_cream_to_add] += 100

    return ice_creams


def test_add_ice_cream():

    pytest.MonkeyPatch().setattr("builtins.input", lambda _: "chocolate")
    assert add_ice_cream() == {"chocolate": 200, "vanilla": 100}


if __name__ == "__main__":
    pytest.main()
