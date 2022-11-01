#WIP
import random


MAX_LINES = 5
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A" : 2,
    "B" : 3,
    "C" : 4,
    "D" : 6,
}

symbol_value = {
    "A" : 5,
    "B" : 4,
    "C" : 3,
    "D" : 2,
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines
            

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) -1:
                print(column[row], end=" | ")
            else:
                print(column[row],end="")
        print()

def deposit():
    """This is the function which will collect the user input for their deposit"""
    while True:
        amount = input("What would you like to deposit? £")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else: print("You have to enter in a number greated than 0")
        else: print("You have to enter in a number")
    return amount

def get_number_of_lines():
    """This is the function which will collect the user input for their lines to bet on"""
    while True:
        lines = input(f"How much lines do you want to be on (1-{MAX_LINES})? ")
        if lines.isdigit():
            lines = int(lines)
            if MAX_LINES >= lines >= 1:
                break
            else: print("You have to enter a valid number")
        else: print("You have to enter in a number")
    return lines

def get_bet():
    """This is the function which will collect the user input for how much they want to bet each line"""
    while True:
        amount = input(f"How much do you want to be on each line? £")
        if amount.isdigit():
            amount = int(amount)
            if MAX_BET >= amount >= MIN_BET:
                break
            else: print(f"You have to enter a number between  £{MIN_BET} and £{MAX_BET}")
        else: print("You have to enter in a number")
    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = lines * bet
        if total_bet > balance:
            print(f"You dont have enough in your balance to bet that much, your current balance is: £{balance}")
        else:
            break

    print(f"You are betting £{bet} on {lines} lines. Your total bet is £{total_bet}")  
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won £{winnings} ")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is £{balance}")
        answer = input("Press enter to spin (q to quit): ")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with £{balance}")
main()
