from secrets import token_hex


occupied_parking_spaces = []

current_parking_space = None
if len(occupied_parking_spaces) >= 255:
    print("There are no more parking spaces available.")
else:
    while (current_parking_space := token_hex(1)) in occupied_parking_spaces:
        print (current_parking_space)
    print("Your parking space is:", current_parking_space)
    occupied_parking_spaces.append(current_parking_space)