file = open(r"GCSE Computer Science\Text Files\Reading Text Files Lesson 1\numbers.txt","r")

numbers_sum = 0
for line in file:
    numbers_sum += int(line)

print(f"{numbers_sum} is the sum of all the numbers in the file.")
