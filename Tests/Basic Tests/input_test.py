import pytest


def pizza_slice_getter():
    print(20 <= 6)
    while True:
        try:
            pizza_slices = int(input("How many slices of pizza would you like? "))

            if 0 < pizza_slices <= 20:
                break
            else:
                raise ValueError("You can only have between 1 and 20 slices of pizza")
        except ValueError:
            raise

    return pizza_slices


def test_pizza_slices(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 5)
    assert pizza_slice_getter() == 5


def test_no_pizza_slices(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 0)
    with pytest.raises(ValueError):
        pizza_slice_getter()
