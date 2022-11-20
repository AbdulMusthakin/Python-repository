from times_table_generator import times_table_generator as ttg


def ttq(max_value, times_table, score):
    """Does the same thing as the times table generator but asks the user the value first and tests;
        if they are correct

    Args:
        max_value (int): the max number the times table will go up to
        times_table (int): the number the times table is about
        score (int): counts how much user got right
    """
    print(f"Here is the {times_table} times table:")
    for i in range(1, max_value):
        answer = i * times_table
        is_valid = False
        while is_valid is False:
            try:
                user_answer = int(input(f"What is {i} * {times_table}?\n"))
                if user_answer == answer:
                    print("You got it right.")
                    score += 1
                elif 0 >= user_answer:
                    raise ValueError
                else:
                    print(
                        f"That's not right. {i} times {times_table} is {answer}")
                is_valid = True
            except ValueError:
                print("You must enter a valid number")
    print(f"You got {score} out of {max_value - 1} right.\
 Thats {round(((score / (max_value - 1)) * 100), 1)}%")


max_value_ttg, times_table_ttg = ttg()
ttq(max_value_ttg, times_table_ttg, 0)
