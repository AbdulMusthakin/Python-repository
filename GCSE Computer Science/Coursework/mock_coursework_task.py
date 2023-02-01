from time import sleep
from datetime import date
from secrets import token_hex

INTRO_HAS_RAN = False

ticket_prices = {
    "adult": 20,
    "child": 12,
    "senior": 11
}


occupied_parking_spaces = []


def intro():
    print("Welcome to the Copington Adventure Theme Park automated ticketing system.",
          "You will be asked a series of questions to determine the price of your ticket.",
          "press any key to continue...", sep="\n")
    input()
    sleep(1)
    main_menu()


def ticket_price_view():
    print("Ticket prices are as follows:",
          ticket_prices,
          "press any key to continue...", sep="\n")
    input()
    sleep(1)
    main_menu()


def purchases():
    valid = False
    adult_tickets = 0
    while valid == False:
        try:
            adult_tickets = int(
                input("How many adult tickets would you like to purchase? "))
            if not 0 <= adult_tickets <= 10:
                print("You can only purchase adult tickets in the range of 0-10.")
                sleep(1)
                raise ValueError
            valid = True
        except ValueError:
            print("Please enter a valid number.")
            sleep(1)

    valid = False
    child_tickets = 0
    while valid == False:
        try:
            child_tickets = int(
                input("How many child tickets would you like to purchase? "))
            if not 0 <= child_tickets <= 20:
                print("You can only purchase child tickets in the range of 0-20.")
                sleep(1)
                raise ValueError
            valid = True
        except ValueError:
            print("Please enter a valid number.")
            sleep(1)

    valid = False
    senior_tickets = 0
    while valid == False:
        try:
            senior_tickets = int(
                input("How many senior tickets would you like to purchase? "))
            if not 0 <= senior_tickets <= 10:
                print("You can only purchase senior tickets in the range of 0-10.")
                sleep(1)
                raise ValueError
            valid = True
        except ValueError:
            print("Please enter a valid number.")
            sleep(1)
    sleep(1)
        
    total_tickets = adult_tickets + child_tickets + senior_tickets
    if total_tickets > 30:
        print("You can only purchase a maximum of 30 tickets. Please try again.")
        sleep(1)
        return purchases()

    if total_tickets == 0:
        print("You must purchase at least 1 ticket. Please try again.")
        sleep(1)
        return purchases()

    valid = False
    total_wristbands = 0
    while valid == False:
        try:
            total_wristbands = int(
                input("How many wristbands would you like to purchase? (1 wristband = £20) "))
            if total_wristbands > total_tickets:
                print("You can only purchase a maximum of 1 wristband per ticket.")
                sleep(1)
                raise ValueError
            if total_tickets < 0:
                sleep(1)
                raise ValueError
            valid = True
        except ValueError:
            print("Please enter a valid number.")
            sleep(1)

    total_price = (adult_tickets * ticket_prices["adult"]) + (
        child_tickets * ticket_prices["child"]) + (senior_tickets * ticket_prices["senior"] + (total_wristbands * 20))
    sleep(1)

    print(
        f"The total price for the tickets (and wristbands) are £{total_price}.")
    sleep(1)

    valid = False
    parking_pass = False
    while valid == False:
        try:
            parking_pass = input("Would you like a parking pass? (y/n) ").lower() == "y"
            if parking_pass == "y" or parking_pass == "n":
                parking_pass = True if parking_pass == "y" else False
                valid = True
                sleep(1)
            else:
                raise ValueError
        except ValueError:
            print("Please enter 'y' for yes or 'n' for no.")
            sleep(1)

    current_parking_space = None
    if parking_pass == True:
        global occupied_parking_spaces
        if len(occupied_parking_spaces) >= 255:
            print("There are no more parking spaces available.")
        else:
            while current_parking_space := token_hex(1) in occupied_parking_spaces:
                pass
            print("Your parking space is:", current_parking_space)
            occupied_parking_spaces.append(current_parking_space)
    sleep(1)

    valid = False
    broker_surname = ""
    while valid == False:
        try:
            broker_surname = input(
                "Please enter the surname of the lead broker: ").capitalize()
            if broker_surname.isalpha():
                valid = True
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid surname.")
            sleep(1)

    sleep(2)
    return total_price, current_parking_space, broker_surname, total_tickets, total_wristbands, 


def payment(price):
    print("Please pay the following amount:", price,
          "This machine only accepts £10 and £20 notes.", sep="\n")
    sleep(2)

    valid = False
    total_paid = 0
    while valid == False:
        try:
            while total_paid < price:
                    ten_pound_notes = int(
                        input("Enter in the amount of £10 notes you are paying with: "))
                    twenty_pound_notes = int(
                        input("Enter in the amount of £20 notes you are paying with: "))
                    
                    total_paid = (ten_pound_notes * 10) + (twenty_pound_notes * 20)
                    sleep(1)
                    if total_paid < price:
                        print("You have not paid enough. Please enter payment again.")
            valid = True
        except ValueError:
            print("Please enter a valid number. Payment will restart.")
    sleep(1)

    change = total_paid - price
    if change > 0:
        print(f"Your change is: £{change}")
    else:
        print("You have paid the exact amount.")
    sleep(2)


def print_ticket(price, pspace, name, tickets, wristbands):
    print("Here is your ticket: \n \n")
    sleep(2)
    print("Tickets Purchased:", tickets)
    print("Wristbands Purchased:", wristbands)
    print("Total Cost:", price)
    print("Lead Broker Surname:", name)
    print("Today's Date:", date.today(), "\n \n")
    sleep(2)
    # Everything below this line is for the parking pass

    if pspace == None:
        print("Enjoy your day at Copington Adventure Theme Park!", "\n \n")
        sleep(2)
        return

    sleep(1)

    print(f"Parking Pass: {name} has been given permission to park in the private car park at {pspace}."
            f"This pass becomes invalid after {date.today()}."
            f"Please ensure that you park in the correct car park.", sep="\n")
    sleep(2)
    print("Enjoy your day at Copington Adventure Theme Park!", "\n \n")
    sleep(2)


def main_menu():
    global INTRO_HAS_RAN
    if INTRO_HAS_RAN == False:
        INTRO_HAS_RAN = True
        intro()

    valid = False
    user_input = 0
    while valid == False:
        try:
            user_input = int(input("Please select an option from the menu below:"
                                   "\n1. See entrance ticket prices"
                                   "\n2. Buy tickets"
                                   "\n> "))
            if user_input == 1 or user_input == 2:
                valid = True
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid option.")
            sleep(1)
    sleep(1)

    if user_input == 1:
        ticket_price_view()

    if user_input == 2:
        print("You will be taken to the ticket purchasing menu.")
        sleep(1)
        total_price, current_parking_space, broker_surname, total_tickets, total_wristbands = purchases()

        print("You will now be taken to the payment menu.")
        sleep(1)
        payment(total_price)

        print("Thank you for your payment. Now you can collect your ticket.")
        sleep(1)
        print_ticket(total_price, current_parking_space, broker_surname,
                     total_tickets, total_wristbands)
        sleep(1)

    INTRO_HAS_RAN = False
    main_menu()


main_menu()
