bill = input("Enter the bill amount: ")

print("Do you want to tip a little, a lot, or not at all?")
tip = input("Enter 'l' for a lot, 's' for a little, or 'n' for not at all: ").lower()

if tip == 'l':
    print(f"Your total bill is ${float(bill) * 1.2}, with a tip of ${float(bill) * 0.2}.")
elif tip == 's':
    print(f"Your total bill is ${float(bill) * 1.1}, with a tip of ${float(bill) * 0.1}.")
elif tip == 'n':
    print(f"Your total bill is ${float(bill)}, with no tip.")
else:
    print("Invalid input.")
