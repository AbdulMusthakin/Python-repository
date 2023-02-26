while True:
    try:
        bill = float(input("What is the total bill? "))
        break
    except ValueError:
        print("Please enter a number")

while True:
    try:
        tip = input("Do you want to leave a tip? (y/n) ").lower()
        if tip not in "yn":
            raise ValueError
        break
    except ValueError:
        print("Please enter y or n")

if tip == "y":
    while True:
        try:
            tip_percent = float(input("What percentage tip do you want to leave? "))
            if tip_percent <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid number")
else:
    tip_percent = 0

tip_amount = bill * (tip_percent / 100)

total = bill + tip_amount

print(f"Tip amount: ${tip_amount:.2f}")

while True:
    try:
        split = input("Are you splitting the bill? (y/n) ").lower()
        if split not in "yn":
            raise ValueError
        break
    except ValueError:
        print("Please enter y or n")

if split == "y":
    while True:
        try:
            people = int(input("How many people are splitting the bill? "))
            if people <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid number")
else:
    people = 1

split_amount = total / people

print(f"Total amount: ${total:.2f}")
print(f"Amount per person: ${split_amount:.2f}")

print("Thank you for using the tip calculator!")
