from time import sleep


print("How much pizza slices do you want?")
while True:
    try:
        pizza_slices = int(input())
        if not 0 < pizza_slices <= 20 or not float(pizza_slices).is_integer():
            raise ValueError
        break
    except ValueError:
        print("Enter in a realistic number")

print("How many people are sharing?")
while True:
    try:
        people = int(input())
        if people <= 0 or not float(people).is_integer():
            raise ValueError
        break
    except ValueError:
        print("Enter a whole number")

slices_per_person = pizza_slices // people
slices_remainder = pizza_slices % people

print(f"Each person gets {slices_per_person} slices")
print(f"And there will be {slices_remainder} slices remaining")
sleep(1)
print("How much does the Pizza cost?")
while True:
    try:
        cost = float(input())
        if cost <= 0:
            raise ValueError
        break
    except ValueError:
        print("Enter a number")

cost_per_slice = round(cost / pizza_slices, 2)
cost_per_person = round(cost_per_slice * slices_per_person, 2)

print(f"One slice of Pizza will cost £{cost_per_slice}")
print(f"So the cost per person is £{cost_per_person}")
