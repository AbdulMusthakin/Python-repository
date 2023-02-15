with open(r"GCSE Computer Science\Text Files\CSV Files\Reading CSV Lesson 1\names.csv", "r+") as file:
    data = file.readlines()
    data = [i.strip("\n") for i in data]
    data.remove("Names")

letter_to_search = input("Please select the letter to search: ").upper()

searched_results = [i for i in data if letter_to_search in i]

print(searched_results)
