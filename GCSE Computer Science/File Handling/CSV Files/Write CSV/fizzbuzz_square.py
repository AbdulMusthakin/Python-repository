fizz_num = int(input("Enter the number to fizz at: "))
buzz_num = int(input("Enter the number to buzz at: "))

list_2d = []
for i in range(0, 100, 10):
    row = []
    for j in range(1, 11):
        string = ""
        if (i + j) % fizz_num == 0:
            string += "fizz"
        if (i + j) % buzz_num == 0:
            string += "buzz"
        if string == "":
            string = str(i + j)
        row.append(string)
       
    list_2d.append(row)

print(list_2d)

with open(r"GCSE Computer Science\Text Files\CSV Files\Writing CSV Lesson 2\fizzbuzz_square.csv", "r+") as file:
    string = ""
    for i in list_2d:
        string += ",".join(i) + "\n"
    file.write(string)
