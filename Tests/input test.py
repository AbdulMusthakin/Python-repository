print(20 <= 6)
print("How much pizza slices do you want?")
while True:
    try:
        pizza_slices = int(input())
        if not 0 < pizza_slices <= 20 or not float(pizza_slices).is_integer():
            raise ValueError
        break
    except ValueError:
        print("Enter in a realistic number")


