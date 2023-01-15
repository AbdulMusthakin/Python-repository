file1 = open(r"GCSE Computer Science\Text Files\Reading Text Files Lesson 1\transcript1.txt","r")

# Print the 6th line of the file
# The enumerate function returns a tuple containing a count (from start which is 0 by default)
# and the values obtained from iterating over a sequence.

mysteryline = ""
for i, line in enumerate(file1):
    if i == 5:
        mysteryline = line.strip()
        break

# Found answer to this from teacher's answers.
# It loops through a string and converts each letter to its ASCII code, then subtracts 2 from it.
# Then it converts the ASCII code back to a letter and adds it to the answer string.

answer = ""
for letter in mysteryline:
    code = ord(letter) - 2
    answer += chr(code)

print(answer)
