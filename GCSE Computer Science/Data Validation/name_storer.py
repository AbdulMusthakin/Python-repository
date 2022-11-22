names_list = []
is_valid = False
q = False
while q is False:
    while is_valid is False:
        try:
            print("Enter a name:")
            name = input()
            if name == "":
                raise ValueError
            names_list.append(name)
            print("Stored name:", name)
            is_valid = True
        except ValueError:
            print("You must enter something")
    q = bool(input("Press enter to move onto next name, or anything to quit\n"))
    is_valid = False
names_list.sort()
print(names_list)
