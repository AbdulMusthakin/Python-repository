print("---Welcome to Split My Bill---")
print("What is the total bill?")
while True:
    try: 
        bill_total = float(input())
        break
    except ValueError:
        print("You need to enter a number")

print("How many people are sharing?")
while True:
    try:
        people = int(input())
        if not float(people).is_integer() or people <= 0:  
            raise ValueError
        break
    except ValueError:
        print("You need to enter in a whole number")

print("What percentage tip would you like to leave?")
while True:
    try:
        tip_percentage = float(input())
        if tip_percentage <= 0:
            raise ValueError
        break
    except ValueError:
        print("You need to enter a percentage")

bill_total += (bill_total * (tip_percentage / 100))
cost_per_person = bill_total / people

print(f"Total bill including tip is £{bill_total}")
print(f"Total cost per person is £{cost_per_person}")