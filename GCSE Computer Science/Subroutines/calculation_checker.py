from time import sleep as sp


def addition(arg1, arg2):
    """Adds two numbers together and returns the result"""
    result = arg1 + arg2
    return result


def subraction(arg1, arg2):
    """Takes away second number from the first and returns the result"""
    result = arg1 - arg2
    return result


def multiplication(arg1, arg2):
    """Multiplies two numbers together and returns the result"""
    result = arg1 * arg2
    return result


def division(arg1, arg2):
    """Divides first number by the second and returns the result"""
    result = arg1 / arg2
    return result


operations = {
    "1": addition,
    "2": subraction,
    "3": multiplication,
    "4": division,
}
operations_symbol = {
    "1": "+",
    "2": "-",
    "3": "*",
    "4": "/",
}

is_valid = True
calculations = 0
while is_valid:
    try:
        calculations = int(
            input("How much calculations do you want to do:")) + 1
        if (calculations - 1) <= 0:
            raise ValueError
        is_valid = False
    except ValueError:
        print("Please enter in a positive integer")
    sp(1)

for _ in range(1, calculations):
    is_valid = True
    while is_valid:
        try:
            num1 = int(input("Enter your first number:"))
            num2 = int(input("Enter your second number:"))
            opp = input(
                "Enter what operation you want(1: add, 2: subtract, 3: multiply, 4: divide):")
            print(
                f"The answer to {num1} {operations_symbol[opp]} {num2}",
                f"is {operations[opp](num1, num2)}")
            is_valid = False
            sp(1)
        except ValueError:
            print("Please enter in an integer")
