with open(r"GCSE Computer Science\Text Files\CSV Files\Reading CSV Lesson 1\weatherdata.csv", "r+") as file:
    data = file.readlines()
    data.remove(data[0])

    data = [i.strip().split(",") for i in data]
    rainfall = [i[5] for i in data]
    max_rainfall = max(rainfall)
    index= rainfall.index(max_rainfall)

print(f"The maximum rainfall was {max_rainfall} on {data[index][0]}")
