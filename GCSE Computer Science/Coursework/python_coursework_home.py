""" This is my attempt at doing my GCSE Computer Science coursework at home. I have to create a program that allows customers to choose the chocolate in their tin."""
# TODO - Annotate the code

NAME_ENTERED = False
TIN_COST = 9.99
DELIVERY_COST = 4.99

# I have stored the flavours in a dictionary so the user can refer to them by both the number and name when ordering.
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
    print("Here are the flavours of chocolates we have:")
    for i in flavours:
        print(f"{i}. {flavours[i]}")
    # This for loop goes through the dictionary and prints the number and name of each flavour
        
    input("Press any key to continue: ")


def get_customer_details():
    customer_name = input("Please enter your name: ").title() # The title method makes the first letter of each word capital, useful for names.
    with open(r"GCSE Computer Science\Text Files\coursework\customer_details.txt", "r+") as file:
        # The r before the string is to make sure the string is a raw string, this is because the backslash is used to escape characters.
        # r+ means that the file is opened for both reading and writing.
        customer_details = file.readlines()
        # Creates a list of the lines in the file.
        total_customers = len(customer_details)
        details_to_add = {total_customers + 1: customer_name}
        # This number is used to identify the customer. It is the number of customers in the file plus 1, as you are adding a new customer.
        file.write(f"{str(details_to_add)} \n")
        # Converts to string so you can add to file, the \n is to make a new line.

def choose_tin_contents():
    user_input = input("If you wish to see the flavours, press '1', otherwise continue: ")
    if user_input == "1":
        view_flavours()
        return choose_tin_contents()
        # The reason it uses return is so all the code below is not executed twice. It ends this execution of the function and starts a new one.
    
    order = {}
    while sum(order.values()) < 1000:
        valid = False
        flavour_to_add = ""
        # This asks the user for an input until they give a valid one.
        while valid == False:
            try:
                flavour_to_add = input("Please either enter the corresponding number or name of the flavour to add: ").title() # All the flavours in the dictionary are stored as first letter uppercase so the input is also made uppercase.
                
                if flavour_to_add.isdigit():
                    # This if statement handles the case where the user enters the number of the flavour.

                    if int(flavour_to_add) in flavours:
                        # This takes the number and accesses the corresponding value in the dictionary. This works since dictionaries are in key-value pairs.

                        if flavours[int(flavour_to_add)] in order:
                            print("test")
                            # This converts the input to a number and then accesses the corresponding value in the dictionary. Then it checks if the user already has this flavour in their tin.
                            # The reason this is nested inside the above if statement is because there could be a key error if the user enters a number that is not in the dictionary.
                            print("You already have this flavour in your tin.")
                            raise ValueError
                        
                        flavour_to_add = flavours[int(flavour_to_add)]
                        valid = True # Makes the while loop end (after it finishes the current iteration).
                    else:
                        print("Please enter a valid number.")
                        raise ValueError
                elif flavour_to_add in flavours.values():
                    # This if statement handles the case where the user enters the name of the flavour.
                    if flavour_to_add in order:
                        print("You already have this flavour in your tin.")
                        raise ValueError                    
                    
                    valid = True # There are two ways to reach valid = True since the user could enter the number or name of the flavour.
                else:
                    print("Please enter a valid flavour.")
                    raise ValueError 
            except ValueError:
                pass # No need to print anything here since all the error messages are in the else statements above.
        
        
        # User can add amount in increments of 100g
        valid = False
        amount_to_add = 0
        # This acts the same as the previous while loop, preventing the user from entering an invalid amount.
        while valid == False:
            try:
                amount_to_add = int(input("Please enter the amount you wish to add (Make sure it is divisible by 100): "))
                
                if amount_to_add <= 0:
                    # Checks if the user has entered a negative number or 0.
                    print("Please enter a valid amount.")
                    raise ValueError

                if not 100 <= amount_to_add <= 500:
                    # This is the range of amounts the user can add for one flavour. They can add 100g, 200g, 300g, 400g or 500g.
                    print("You have to have at least 100g and no more than 500g.")
                    raise ValueError
                
                if sum(order.values()) + amount_to_add > 1000:
                    # The maximum amount of chocolate the user can have is 1000g.
                    print("You cannot have more than 1000g of chocolate.")
                    raise ValueError
                
                
                
                if amount_to_add % 100 == 0:
                    # They can only add amounts in increments of 100g.
                    user_input = input(f"You have chosen to add {amount_to_add}g of {flavour_to_add}. Press 'y' to confirm, otherwise retry: ").lower()
                    if user_input == "y":
                        # Lets the user confirm their choice.
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
        # The update method adds the flavour and amount to the dictionary as a key-value pair.
    
    if 3 <= len(order) <= 6:
        # The user can have between 3 and 5 flavours in their tin.
        print("Your order is complete.")
        return order
    else:
        print("You must have between 3 and 6 flavours. Resetting order.")
        return choose_tin_contents()

def store_order(order):
    with open(r"GCSE Computer Science\Text Files\coursework\customer_details.txt", "r+") as file:
        lines = file.readlines()
        last_line = lines[-1] # Gets the last line in the file.
        # Add order to the last line.
        last_line = last_line[:-2] # Removes the newline character
        last_line += f", {str(order)}\n" # Adds the order to the last line.
        lines[-1] = last_line # Replaces the last line with the new one.
        file.seek(0) # Goes to the start of the file.
        file.writelines(lines) # Writes the new lines to the file.
        
        
        

def choose_personalised_message():
    user_input = input("Would you like to add a personalised message? Press 'y' for yes, otherwise press any other key: ").lower()
    if user_input == "y":
        message = input("Please enter your message: ")
        return message
    else:
        print("Returning to main menu.")
        return ""
 

def create_invoice(order, message, full_message, tin_cost=TIN_COST, delivery_cost=DELIVERY_COST):
    
    # First, we remove the whitespace from the message and then calculate the cost of the message.
    message.replace(" ", "") # Replace all the whitespace with nothing.
    message_cost = (len(message) * 0.10).__round__(2) # Each character costs 10p.
    # The __round__ method rounds the number to 2 decimal places. We do this because Python does something called floating point arithmetic, which can give us some weird results (e.g. 0.1 + 0.2 = 0.30000000000000004)
    total_cost = (tin_cost + delivery_cost + message_cost).__round__(2)
    
    # This prints the invoice.
    
    invoice = f"Tin cost: £{tin_cost} \nDelivery cost: £{delivery_cost} \nCost of message: £{message_cost} \nTotal cost: £{total_cost} \nMessage:\n{full_message}"

    return invoice
    

def main_menu():
    # First we will have the customer enter and store their details.
    # This makes it so the customer is only asked for their details once.
    global NAME_ENTERED
    if NAME_ENTERED == False:  # Set to False at the start of the program and set to True after the customer has entered their details.
        get_customer_details()
        NAME_ENTERED = True
        

    user_input = input(
        "Press '1' to view the flavours of chocolates. Press '2' to choose the contents of your tin. Press '3' to exit:\n> ")

    if user_input == "1":
        view_flavours()
        # Main menu is called again, otherwise the program would end.
        main_menu()
    elif user_input == "2":
        order = choose_tin_contents()
        print(f"Your order is:\n{order}")
        
        store_order(order)
        
        message = choose_personalised_message()
        full_message = "Merry Christmas,\n" + message
        
        # Calculate the cost of the order and gives an invoice.
        invoice = create_invoice(order, message, full_message)
        # I decided against having two seperate functions since I would have to return everything from the cost function and then pass it to the invoice function.
        
        "Your invoice is:\n"
        print(invoice)
        
    elif user_input == "3":
        pass # Everything in the function after this is in an else statement so it will not be executed if this is and the program will exit.
    else:
        print("Please enter a valid input.")
        main_menu()
        # I could have used a while loop with a try-except block but since there is nothing else in the function besides an if statement (and another if statement but that only runs once),
        # I can restart it if the user enters an invalid input.


main_menu() # The program is entirely modular, it all runs off the main_menu function and there is only one line of code outside functions.
