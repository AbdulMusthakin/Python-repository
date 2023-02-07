flavours = ["Caramel Twist",
            "Orange Crush",
            "Chocolate Bar",
            "Brazil Nut in Chocolate",
            "Cornish Fudge",
            "Strawberry Treat",
            "Orange Smoothie",
            "Toffee Bar",
            "Hazelnut Triangle",
            "Coconut Dream"
            ]


def view_flavours():
    print(f"Here are the flavours of chocolates we have: \n{flavours}")
    input("Press any key to continue: ")


def get_customer_details():
    customer_name = input("Please enter your name: ").title()
    with open(r"GCSE Computer Science\Text Files\coursework\customer_details.txt", "r+") as file:
        customer_details = file.readlines()
        total_customers = len(customer_details)
        details_to_add = {total_customers + 1: customer_name}
        file.write(f"{str(details_to_add)} \n")


def choose_tin_contents():
    pass


def main_menu():
    # First we will have the customer enter and store their details
    get_customer_details()

    # The customer can view the different flavours of chocolates or chooce their tin contents

    user_input = input(
        "Press '1' to view the flavours of chocolates. Press '2' to choose the contents of your tin. Press '3' to exit:\n>")

    if user_input == "1":
        view_flavours()
    if user_input == "2":
        choose_tin_contents()
    if user_input == "3":
        pass


main_menu()
