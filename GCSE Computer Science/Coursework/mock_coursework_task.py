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
    sleep(2)
    main_menu()


def ticket_price_view():
    print("Ticket prices are as follows:",
          ticket_prices,
          "press any key to continue...", sep="\n")
    input()
    sleep(2)
    main_menu()


def purchases():
    adult_tickets = int(
        input("How many adult tickets would you like to purchase? "))
    child_tickets = int(
        input("How many child tickets would you like to purchase? "))
    senior_tickets = int(
        input("How many senior tickets would you like to purchase? "))
    total_tickets = adult_tickets + child_tickets + senior_tickets

    total_wristbands = int(
        input("How many wristbands would you like to purchase?"))

    total_price = (adult_tickets * ticket_prices["adult"]) + (
        child_tickets * ticket_prices["child"]) + (senior_tickets * ticket_prices["senior"] + (total_wristbands * 20))
    sleep(1)

    print(
        f"The total price for the tickets (and wristbands) are £{total_price}.")

    parking_pass = True if input(
        "Would you like a parking pass? (y/n)".lower()) == "y" else False

    broker_surname = input(
        "Please enter the surname of the lead broker: ").capitalize()

    sleep(2)
    return total_price, parking_pass, broker_surname, total_tickets, total_wristbands


def payment(price):
    print("Please pay the following amount:", price,
          "This machine only accepts £10 and £20 notes.", sep="\n")
    sleep(2)
    total_paid = 0
    while total_paid < price:
        ten_pound_notes = int(
            input("Enter in the amount of £10 notes you are paying with:"))
        twenty_pound_notes = int(
            input("Enter in the amount of £20 notes you are paying with:"))
        total_paid = (ten_pound_notes * 10) + (twenty_pound_notes * 20)
        sleep(1)
        if total_paid < price:
            print("You have not paid enough. Please enter payment again.")
    sleep(1)
    change = total_paid - price
    if change > 0:
        print("Your change is:", change)
    else:
        print("You have paid the exact amount.")

    sleep(1)
    print("Thank you for your payment. Now you can collect your ticket.")
    sleep(2)


def print_ticket(price, ppass, name, tickets, wristbands):
    print("Here is your ticket:")
    sleep(2)
    print("Tickets:", tickets)
    print("Wristbands:", wristbands)
    print("Price:", price)
    print("Lead Broker Surname:", name)
    print("Today's Date:", date.today())
    sleep(2)
    # Everything below this line is for the parking pass
    global occupied_parking_spaces

    current_parking_space = token_hex(2)
    while current_parking_space in occupied_parking_spaces:
        current_parking_space = token_hex(2)
    occupied_parking_spaces.append(current_parking_space)

    if len(occupied_parking_spaces) > 255:
        print("There are no more parking spaces available.")
        ppass = False
    sleep(1)
    if ppass == True:
        print(f"Parking Pass: {name} has been given permission to park in the private car park at {current_parking_space}."
              f"This pass becomes invalid after {date.today()}."
              f"Please ensure that you park in the correct car park.")
    sleep(2)
    print("Enjoy your day at Copington Adventure Theme Park!")
    sleep(2)


def main_menu():
    global INTRO_HAS_RAN
    if INTRO_HAS_RAN == False:
        INTRO_HAS_RAN = True
        intro()

    user_input = 2
    int(input("Please select an option from the menu below:"
              "\n1. See entrance ticket prices"
              "\n2. Buy tickets"
              "\n3. Exit"
              "\n> "))
    sleep(1)
    if user_input == 1:
        ticket_price_view()
    elif user_input == 2:
        sleep(1)
        total_price, parking_pass, broker_surname, total_tickets, total_wristbands = purchases()
        sleep(1)
        payment(total_price)
        sleep(1)
        print_ticket(total_price, parking_pass, broker_surname,
                     total_tickets, total_wristbands)
        sleep(1)
    # INTRO_HAS_RAN = False
    main_menu()


main_menu()
