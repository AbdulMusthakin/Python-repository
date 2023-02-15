numbers = [str(i) for i in range(1,21)]
# I have used a list comprehension to create a list of string numbers from 1-20(including 20)

str_numbers = ",".join(numbers)
with open(r"GCSE Computer Science\Text Files\CSV Files\Writing CSV Lesson 2\numbers.csv", "r+") as file:
    file.truncate(0) # This is a way of clearing contents of file when opening in r+ mode
    file.write(str_numbers)
    file.seek(0) # When I write to a file it goes to the end so I use seek to go to the beginning to be able to read from there
    print(file.read())
