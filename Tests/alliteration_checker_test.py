def check_alliteration(string):
    prev_char = None
    for char in string:
        if char == prev_char:
            return True
        prev_char = char
    return False


alliteration_examples = ["Bob bakes bread",
                         "Sally sings a song", "soob nob dob"]
for example in alliteration_examples:
    if check_alliteration(example):
        print(f"'{example}' has alliteration")
    else:
        print(f"'{example}' does not have alliteration")
# The above code does not work, it doesn't check for alliteration
# what it does is check if two adjacent characters are the same
# This code was given by Chatgpt
# Can Github autopilot do better?
# Write code to check if a string has alliteration


def alliteration_checker(string):
    # write function docstring
    """Checks if a string has alliteration
    Args: string (str): string to check
    Returns: bool: True if string has alliteration, False otherwise"""
    string = string.lower()
    string = string.split()
    for i in range(len(string)-1):
        if string[i][0] == string[i+1][0]:
            return True
    return False


alliteration_examples = ["Bob bakes bread",
                         "Sally sings a song", "soob nob dob"]
for example in alliteration_examples:
    if alliteration_checker(example):
        print(f"'{example}' has alliteration")
    else:
        print(f"'{example}' does not have alliteration")

# The above code works, it checks for alliteration
# write what the split method does
"""The split method splits a string into a list of strings
by separating the string where there are spaces"""