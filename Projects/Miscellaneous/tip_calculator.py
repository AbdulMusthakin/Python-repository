bill = input("Enter the bill amount: ")

print("Do you want to tip a little, a lot, or not at all?")
# Check if they entered a money symbol and remove it if they did
if bill[0] in "$£€¥₹₽₿":
    remove = bill[0]
    bill = bill.replace(remove, "")

tip = input("Enter 'l' for a lot, 's' for a little, or 'n' for not at all: ").lower()


total_bill = 0
if tip == 'l':
    total_bill = float(bill) * 1.2
elif tip == 's':
    total_bill = float(bill) * 1.1
elif tip == 'n':
    total_bill = float(bill)
else:
    print("Invalid input.")

print(f"Your total bill is ${total_bill:.2f}.")

print("Do you want to split the bill?")
split = input("Enter 'y' for yes or 'n' for no: ").lower()
if split == 'y':
    
    amount_of_people = input("How many people are splitting the bill? ")
    amount_per_person = float(total_bill) / int(amount_of_people)
    print(f"Each person should pay ${amount_per_person:.2f}.")
elif split == 'n':
    print("Okay, no problem.")
else:
    print("Invalid input.")
    
print("Thank you for using the tip calculator.")