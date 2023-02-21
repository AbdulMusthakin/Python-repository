""" This is my attempt at doing my GCSE Computer Science coursework at home. I have to create a program that allows customers to choose the chocolate in their tin."""
# TODO - Annotate the code

NAME_ENTERED = False

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

print(flavours.keys())
print(flavours.values())

def view_flavours():
    print("Here are the flavours of chocolates we have:")
    for i in flavours:
        print(f"{i}. {flavours[i]}")
          
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
        return choose_tin_contents()
    
    order = {}
    while sum(order.values()) < 1000:
        valid = False
        flavour_to_add = ""
        while valid == False:
            try:
                flavour_to_add = input("Please either enter the corresponding number or name of the flavour to add: ").title()
                
                if flavour_to_add.isdigit():
                    
                    if int(flavour_to_add) in flavours:
                        flavour_to_add = flavours[int(flavour_to_add)]
                        valid = True
                    else:
                        print("Please enter a valid number.")
                        raise ValueError
                
                if flavour_to_add in flavours.values():
                    valid = True
                else:
                    print("Please enter a valid flavour.")
                    raise ValueError 
            except ValueError:
                pass
        
        # User can add amount in increments of 100g
        
        valid = False
        amount_to_add = 0
        while valid == False:
            try:
                amount_to_add = int(input("Please enter the amount you wish to add (Make sure it is divisible by 100): "))
                
                if amount_to_add <= 0:
                    print("Please enter a valid amount.")
                    raise ValueError

                if 100 <= amount_to_add <= 500:
                    pass 
                else:
                    print("You have to have at least 100g and no more than 500g.")
                    raise ValueError
                
                if amount_to_add % 100 == 0:
                    user_input = input(f"You have chosen to add {amount_to_add}g of {flavour_to_add}. Press 'y' to confirm, otherwise retry: ").lower()
                    if user_input == "y":
                        valid = True
                    else:
                        raise ValueError
                else:
                    print("Please enter a valid amount.")
                    raise ValueError

                valid = True
            except ValueError:
                pass
        
        order.update({flavour_to_add: amount_to_add})
    
    return order

 
def main_menu():
    # First we will have the customer enter and store their details
    global NAME_ENTERED
    if NAME_ENTERED == False:
        get_customer_details()
        NAME_ENTERED = True
        

    # The customer can view the different flavours of chocolates or chooce their tin contents

    user_input = input(
        "Press '1' to view the flavours of chocolates. Press '2' to choose the contents of your tin. Press '3' to exit:\n> ")

    if user_input == "1":
        view_flavours()
        main_menu()
    if user_input == "2":
        order = choose_tin_contents()
        print(order)
    if user_input == "3":
        pass


main_menu()
