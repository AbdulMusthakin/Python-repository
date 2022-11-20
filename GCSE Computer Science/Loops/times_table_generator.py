def times_table_generator():
    """
    Asks user for a number to find the product of and iterates it from 1 to the max value given
    """
    is_valid = False
    times_table = 0
    while is_valid is False:
        try:
            times_table = int(input("What number do you want the times table of? \n"))
            if times_table <= 0:
                raise ValueError
            is_valid = True
        except ValueError:
            print("You must enter a number more than 0")
    is_valid = False
    max_value = 0
    while is_valid is False:
        try:
            max_value = int(input("What do you want to go up to(number * upper_bound)? \n")) + 1
            if max_value <= 1:
                raise ValueError
            is_valid = True
        except ValueError:
            print("You must enter a number above 1")
    return max_value, times_table
