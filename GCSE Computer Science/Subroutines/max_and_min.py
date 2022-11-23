def max_value(arg1, arg2):
    """

    Args:
        arg1 (int): the first number
        arg2 (int): the second number

    Returns:
        int: the larger number
    """
    if arg1 > arg2:
        result = arg1
    elif arg1 < arg2:
        result = arg2
    else:
        result = None
    return result

def min_value(arg1, arg2, arg3):
    """finds the smaller of three numbers

    Args:
        arg1 (int): the first number
        arg2 (int): the second number
        arg3 (int): the third number
    Returns:
        int: the smaller number
    """
    if arg1 < arg2 and arg1 < arg3:
        result = arg1
    elif arg2 < arg1 and arg2 < arg3:
        result = arg2
    elif arg3 < arg2 and arg3 < arg1:
        result = arg3
    else:
        result = None
    return result

a = int(input("Enter a number:"))
b = int(input("Enter another number:"))
c = int(input("Enter one more number:"))
print(f"The smallest number entered is {min_value(a,b,c)}")
