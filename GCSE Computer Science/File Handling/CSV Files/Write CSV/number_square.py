list_2d = [[str(i + j) for j in range(1, 11)] for i in range(0, 100, 10)]

with open(r"GCSE Computer Science\Text Files\CSV Files\Writing CSV Lesson 2\number_square.csv", "r+") as file:
    string = ""
    for i in list_2d:
        string += ",".join(i) + "\n"
    file.write(string)
