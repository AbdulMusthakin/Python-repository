# print("You must enter a number:")
# try:
# except ValueError:
# print("Enter a number:")
# not_validated = True
# while not_validated:
# number = int(input())
# not_validated = False

# Rearanged:
not_validated = True
while not_validated:
    try:
        print("Enter a number:")
        number = int(input())
        not_validated = False
    except ValueError:
        print("You must enter a number:")
    