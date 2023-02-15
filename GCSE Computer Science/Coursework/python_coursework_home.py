flavours = {1: "Caramel Twist",
            2: "Orange Crush",
            3: "Chocolate Bar",
            4: "Brazil Nut in Chocolate",
            5: "Cornish Fudge",
            6: "Strawberry Treat",
            7: "Orange Smoothie",
            8: "Toffee Bar",
            9: "Hazelnut Triangle",
            10: "Coconut Dream"
            }


def view_flavours():
    print(f"Here are the flavours of chocolates we have: \n{flavours.values()}")
    input("Press any key to continue: ")


def get_customer_details():
    customer_name = input("Please enter your name: ").title()
    with open(r"GCSE Computer Science\Text Files\coursework\customer_details.txt", "r+") as file:
        customer_details = file.readlines()
        total_customers = len(customer_details)
        details_to_add = {total_customers + 1: customer_name}
        file.write(f"{str(details_to_add)} \n")


def choose_tin_contents():
    user_input = input("If you wish to see the flavours, press '1', otherwise continue: ")
    if user_input:
        view_flavours()
        return choose_tin_contents()x
    
    valid = False
    flavour_to_add = ""
    while valid == False:
        try:
            flavour_to_add = input("Please either enter the corresponding number or name of the flavour to add: ")

            if flavour_to_add.title() not in flavours.values():
                print("Sorry, we don't recognsie that flavour. Please try again.")
                raise ValueError

            if flavour_to_add not in flavours.keys():
                print("Sorry, we don't recognsie that flavour. Please try again.")
                raise ValueError
            else:
                confirm = input(f"You have chosen {flavour_to_add}. Press 'y' to confirm, otherwise retry: ").lower()
                if confirm == "y":
                    valid = True
                else:
                    raise ValueError
            
            if flavour_to_add.isdigit():
                flavour_to_add = int(flavour_to_add)
                confirm = input(f"You have chosen {flavours[flavour_to_add]}. Press 'y' to confirm, otherwise retry: ").lower()
                if confirm == "y":
                    valid = True
                else:
                    raise ValueError
        except ValueError:
            pass
    

 
def main_menu():
    # First we will have the customer enter and store their details
    get_customer_details()

    # The customer can view the different flavours of chocolates or chooce their tin contents

    user_input = input(
        "Press '1' to view the flavours of chocolates. Press '2' to choose the contents of your tin. Press '3' to exit:\n> ")

    if user_input == "1":
        view_flavours()
    if user_input == "2":
        choose_tin_contents()
    if user_input == "3":
        pass


main_menu()
