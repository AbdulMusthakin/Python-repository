from secrets import token_hex
import pytest


occupied_parking_spaces = []

current_parking_space = None


def parking_space():
    current_parking_space = None
    if len(occupied_parking_spaces) >= 255:
        print("There are no more parking spaces available.")
    else:
        while (current_parking_space := token_hex(1)) in occupied_parking_spaces:
            print(current_parking_space)
        print("Your parking space is:", current_parking_space)
        occupied_parking_spaces.append(current_parking_space)

    return current_parking_space


def test_parking_space():
    assert parking_space() != None
    assert len(occupied_parking_spaces) == 1
