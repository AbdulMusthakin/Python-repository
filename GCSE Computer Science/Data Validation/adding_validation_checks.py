is_valid = False
while is_valid is False:
    try:
        print("Enter a number between 1 and 10:")
        number = int(input())
        if not 0 < number <= 10:
            raise ValueError
        is_valid = True
    except ValueError:
        print("You must enter a number between 1 and 10:")
        number = int(input())
