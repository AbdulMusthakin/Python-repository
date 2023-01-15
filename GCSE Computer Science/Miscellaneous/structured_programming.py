def num_dogs():
    while True:
        try:
            dogs = int(input("How many dogs were walked? In digits. "))
            if dogs <= 3:
                break
            print("Maximum 3 dogs.")
        except ValueError:
            print("Invalid input.")
    return dogs

def num_days():
    while True:
        try:
            days = int(input("How many days were they walked? In digits. "))
            break
        except ValueError:
            print("Invalid input.")
    return days

def num_walks(dogs, days):
    walks = dogs*days
    return walks

def total_charge(walks):
    cost = walks*4
    return cost

def user_name():
    while True:
        try:
            name = input("What is the name of the client? ")
            if name.isalpha():
                break
            print("Invalid input.")
        except ValueError:
            print("Invalid input.")
    return name

def invoice(dogs, days, walks, cost, name):
    print(f"There were {dogs} dogs, walked for {days} days for a total of {walks}"
    ,f"walks, at £4.00 per walks this costs £{cost}. The client is {name}.")

total_dogs = num_dogs()
total_days = num_days()
total_walks = num_walks(total_dogs,total_days)
total_cost = total_charge(total_walks)
client_name = user_name()
invoice(total_dogs, total_days, total_walks, total_cost, client_name)
