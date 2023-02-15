"""
with open(r"GCSE Computer Science\Text Files\CSV Files\Reading CSV Lesson 1\players.csv", "r+") as file:
    data = file.readlines()
    data.remove(data[0])
    data = [i.strip().split(",") for i in data]


user_input = input("Enter a player name: ")
player_score = str([i[1] for i in data if i[0] ==
                   user_input]).strip("[]").strip("'")
'''
The above list compehension is equivalent to:
for i in data:  
    if i[0] == user_input:
        player_score = i[1]
player_score = str(player_score).strip("[]").strip("'")
'''


print(f"The player's score is: {player_score}")
"""

# Explorer Task

with open(r"GCSE Computer Science\Text Files\CSV Files\Reading CSV Lesson 1\players.csv", "r+") as file:
    data = file.readlines()
    data.remove(data[0])
    
    data = {i.strip().split(",")[0] : int(i.strip().split(",")[1]) for i in data}
    print(data)

"""
What the dictionary comprehension looks as a for loop:

dict_data = {}
for i in data:
    i = i.strip().split(",")
    data[i[0]] = int(i[1])
    dict_data[i[0]] = int(i[1])
"""