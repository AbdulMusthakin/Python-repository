import pytest

# create a powersum function
def powersum(power, *args):
    """Return the sum of each argument raised to specified power."""
    total = 0
    for i in args:
        total += pow(i, power)
    return total


def test_powersum():
    assert powersum(2, 3, 4) == 25
    assert powersum(2, 10) == 100
