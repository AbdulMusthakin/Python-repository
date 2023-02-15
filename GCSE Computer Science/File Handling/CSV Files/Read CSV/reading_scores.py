with open(r"GCSE Computer Science\Text Files\CSV Files\Reading CSV Lesson 1\scores.csv", "r+") as file:
    data = file.readlines()
    data = [i.strip('\n') for i in data]
    
    for i in data:
        if not i.isdigit():
            data.remove(i)

    data = [int(i) for i in data]
    print("max number:", max(data))
    print("min number:", (min(data)))
    
    average = sum(data) / len(data)
    print("average:", average)
