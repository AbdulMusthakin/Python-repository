"""This is my attempt at making the coursework with some more advanced techniques."""
from time import sleep
import os
import pickle

TIN_COST = 9.99
DELIVERY_COST = 4.99

flavours = {
    1: "Caramel Twist",
    2: "Orange Crush",
    3: "Chocolate Bar",
    4: "Brazil Nut in Chocolate",
    5: "Cornish Fudge",
    6: "Strawberry Treat",
    7: "Orange Smoothie",
    8: "Toffee Bar",
    9: "Hazelnut Triangle",
    10: "Coconut Dream",
}


def view_flavours():
    print("Here are the flavours of chocolates we have:")
    for i in flavours:
        print(f"{i}. {flavours[i]}")
        sleep(0.5)
    # This for loop goes through the dictionary and prints the number and name of each flavour

    input("Press any key to continue: ")


def load_orders():
    with open(
        r"GCSE Computer Science\Text Files\coursework\adv_customer_details.txt", "rb"
    ) as f:
        try:
            orders = pickle.load(f)
        except EOFError:
            return []
        else:
            return orders


class Order:
    def __init__(
        self,
        customer_name="",
        order_details={},
        order_cost=0,
        message="",
        total_orders=[],
    ):
        self.name = customer_name
        self.order = order_details
        self.cost = order_cost
        self.message = message
        self.total_orders = total_orders

    def __str__(self):
        return f"Name: {self.name}\nOrder: {self.order}\nCost: {self.cost}\nMessage: {self.message}"

    def get_customer_name(self):
        valid = False
        while not valid:
            try:
                self.name = input("Please enter your name: ").title()
                sleep(1)
                if (self.name.replace(" ", "")).isalpha() == False:
                    # isalpha() returns True if all the characters in the string are letters, and if there is at least one character.
                    # We use replace to remove any spaces in the name, otherwise it would return False if the user entered their full name.
                    print("Please enter a valid name.")
                    sleep(1)
                    raise ValueError
                valid = True
            except ValueError:
                pass

        if self.name.lower() == "admin":
            return admin_menu()

    def choose_tin_contents(self, flavours=flavours):
        user_input = input(
            "Press 1 to view flavours, press any other key to continue: "
        )
        sleep(1)

        if user_input == "1":
            view_flavours()
            return self.choose_tin_contents()  # So function doesn't recurse

        self.order = {}
        while sum(self.order.values()) < 1000:
            # First get flavour of chocolate

            valid = False
            flavour_to_add = ""
            while not valid:
                try:
                    print(
                        "Please enter the number or name of the flavour you would like to add."
                    )
                    flavour_to_add = input("> ").title()
                    sleep(1)

                    if flavour_to_add.isdigit():
                        # Handles is user enters in number

                        if flavours[int(flavour_to_add)] in self.order:
                            print("You already have this flavour in your tin.")
                            sleep(1)
                            raise ValueError

                        flavour_to_add = flavours[int(flavour_to_add)]
                        valid = True

                    elif flavour_to_add in flavours.values():
                        # Handles if user enters in name of flavour

                        if flavour_to_add in self.order:
                            print("You already have this flavour in your tin.")
                            sleep(1)
                            raise ValueError

                        valid = True

                    else:
                        print("Please enter a valid flavour.")
                        sleep(1)
                        raise ValueError

                except ValueError:
                    pass
                    # pass because error messages are handled in the try block

            # Now get quantity of flavour
            valid = False
            amount_to_add = 0
            while not valid:
                try:
                    print(f"How many grams of {flavour_to_add} would you like to add?")
                    print("Note: Make sure it is divisible by 100.")

                    amount_to_add = int(input("> "))
                    sleep(1)

                    if not 100 <= amount_to_add <= 500:
                        print(
                            "You can only add between 100 and 500 grams of each flavour."
                        )
                        sleep(1)
                        raise ValueError

                    if sum(self.order.values()) + amount_to_add > 1000:
                        print(
                            "You can only have up to 1000 grams of chocolate in your tin."
                        )
                        sleep(1)
                        raise ValueError

                    if amount_to_add % 100 == 0:
                        print(
                            f"You have added {amount_to_add} grams of {flavour_to_add}."
                        )
                        sleep(1)
                        print(
                            "Are you sure this is correct? Press 'y' to confirm. Otherwise restart."
                        )
                        confrimation = input("> ").lower()
                        sleep(1)

                        if confrimation == "y":
                            valid = True
                        else:
                            print("You can pick a different amount.")
                            sleep(1)
                            raise ValueError

                except ValueError:
                    pass

            self.order.update({flavour_to_add: amount_to_add})

        if 3 <= len(self.order) <= 6:
            print("Order complete.")
            sleep(1)
        else:
            print("You must have between 3 and 6 flavours in your tin.")
            sleep(1)
            self.choose_tin_contents()

    def choose_message(self):
        print(
            "\nYou can add a personalised message to your tin. This includes 'Merry Christmas', then the recipient's name and anythign esle you want to add."
        )
        print(
            "Note: 'Merry Christmas' is free but every other character costs 10p, not including spaces."
        )
        sleep(1)

        print(
            "Would you like to add a message? Press 'y' to confirm. Otherwise press any other key."
        )
        user_input = input("> ").lower()
        sleep(1)

        if user_input == "y":
            recipient_name = input("Please enter the recipients name: ").title()
            sleep(1)

            additional_msg = input(
                "Please enter any additional message you would like to add, or enter nothing: "
            )
            sleep(1)

            if additional_msg != "":
                self.message = f"{recipient_name}. {additional_msg}"
            else:
                self.message = recipient_name
        else:
            print("Returning to main menu.")
            sleep(1)
            self.message = ""

    def __list__(self):
        return [self.name, self.order, self.message, self.cost]

    def store_order(self):
        with open(
            r"GCSE Computer Science\Text Files\coursework\adv_customer_details.txt",
            "rb+",
        ) as f:
            if self.message == "":
                self.message = "None"

            self.total_orders.append(self.__list__())
            pickle.dump(self.total_orders, f)

    def cost_and_invoice(
        self, full_message, tin_cost=TIN_COST, delivery_cost=DELIVERY_COST
    ):

        no_space_message = self.message.replace(" ", "")

        message_cost = round(len(no_space_message) * 0.1, 2)

        self.cost = round(tin_cost + delivery_cost + message_cost, 2)

        invoice = f"Tin cost: £{tin_cost} \nDelivery cost: £{delivery_cost} \nCost of message: £{message_cost:.2f} \nTotal cost: £{self.cost} \nMessage:\n{full_message}"

        return invoice


def admin_menu(password="password"):
    print("Enter Password to access admin menu.")
    entered_pass = input("> ")
    if entered_pass != password:
        print("Incorrect. Exiting...")

        exit()

    while True:
        os.system("cls")
        print("Welcome to the admin menu!")
        print("Press 1 to search for customer details by order number.")
        print("Press 2 to retrieve all customer orders for preparation and despatch.")
        print("Press 3 to exit.")

        user_input = input("> ")

        if user_input == "1":
            search_by_order()
        elif user_input == "2":
            prepare_for_despatch()
        elif user_input == "3":
            print("Exiting...")
            sleep(1)
            exit()
        else:
            print("Please enter a valid option.")
            sleep(1)


def search_by_order():
    valid = False
    user_input = 0
    while not valid:
        try:
            print("Enter the order number you would like to search for.")
            user_input = int(input("> "))
            sleep(1)

            if user_input <= 0:
                print("Please enter a valid order number.")
                sleep(1)
                raise ValueError

            if user_input > len(load_orders()):
                print("Order not found.")
                sleep(1)
                raise ValueError

            valid = True
        except ValueError:
            pass

    order_to_search = load_orders()[user_input - 1]
    print("What details would you like to view?")
    print("Press 1 to view customer name.")
    print("Press 2 to view tin contents.")
    print("Press 3 to view message.")
    print("Press 4 to view cost.")
    print("Press 5 to go back to the admin menu.")

    valid = False
    detail_to_view = ""
    while not valid:
        try:
            detail_to_view = input("> ")
            sleep(1)

            if detail_to_view not in ["1", "2", "3", "4", "5"]:
                print("Please enter a valid option.")
                sleep(1)
                raise ValueError

            if detail_to_view == "1":
                print(f"Customer name: {order_to_search[0]}")
                sleep(1)
            elif detail_to_view == "2":
                print(f"Tin contents: {order_to_search[1]}")
                sleep(1)
            elif detail_to_view == "3":
                print(f"Message: {order_to_search[2]}")
                sleep(1)
            elif detail_to_view == "4":
                print(f"Cost: £{order_to_search[3]}")
                sleep(1)
            elif detail_to_view == "5":
                valid = True
            else:
                print("Please enter a valid option.")
                sleep(1)
                raise ValueError
        except ValueError:
            pass

    sleep(1)


def prepare_for_despatch():
    print("Preparing orders for despatch...")
    sleep(1)
    total_cost = 0
    for order in load_orders():
        # Find total cost of order
        cost = order[3]
        total_cost += cost

    # Create dictionary with all flavours and set to 0
    flavours_needed = {flavours[i]: 0 for i in flavours}

    for order in load_orders():
        # Find all flavours needed
        for flavour, amount in order[1].items():
            flavours_needed[flavour] += amount
    sleep(1)

    print("Total cost of all orders: £", total_cost)
    sleep(1)

    for i in flavours_needed:
        print(f"{i}: {flavours_needed[i]}")
        sleep(0.5)

    input("Press enter to return to admin menu.")

    sleep(1)


def main_menu(order, name_entered=True):
    if not name_entered:
        order.total_orders = load_orders()

        order.get_customer_name()

    os.system("cls")
    print("Welcome to Park Vale Chocolates!")
    sleep(1)
    print("Press 1 to view flavours, press 2 to choose contents of tin.")

    user_input = input("> ")

    if user_input == "1":
        view_flavours()
        sleep(1)
        main_menu(order)
    elif user_input == "2":
        order.choose_tin_contents()
        print("Your tin contains:")
        print(order.order)
        sleep(2)

        order.choose_message()

        full_message = ""
        if order.message != "":
            full_message = "Merry Christmas,\n" + order.message
        else:
            full_message = "No message provided."

        sleep(1)

        invoice = order.cost_and_invoice(full_message)

        sleep(1)
        order.store_order()
        sleep(1)

        print("\nYour invoice is:")
        print(invoice)

    else:
        print("Please enter a valid option.")
        sleep(1)
        main_menu(order)


if __name__ == "__main__":
    main_menu(order=Order(), name_entered=False)
