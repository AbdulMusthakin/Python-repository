def average(*args):
    """Function that finds the average of an undspecified amount of values"""
    result = sum(
        args)/len(args)  # sum finds the total in the iterable and len finds how much elements in it
    print(args) # args is a tuple which is iterable
    print(result)


#average(1, 2, 3)
user_inputs = {}
x = 1
nums = 0
while True:
    try:
        nums = input("enter a number (or 'q' to quit):")
        if nums == "q".lower():
            break
        if not nums.isdigit():
            raise ValueError
        user_inputs[f"num{x}"] = int(nums)
        x += 1
    except ValueError:
        print("You must enter an integer")
num_tuple = tuple(user_inputs.values())
average(*num_tuple)
