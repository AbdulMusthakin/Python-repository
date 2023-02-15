num_times_tables = int(input("What number times table do you want? "))
upper_limit = int(input("What number do you want to go up to? "))

times_tables_list = [str(num_times_tables * i) for i in range(1, upper_limit + 1)]
str_times_tables_list = ",".join(times_tables_list)

with open(r"GCSE Computer Science\Text Files\CSV Files\Writing CSV Lesson 2\times_tables.csv" , "r+") as file:
    file.write(f"{str_times_tables_list}")
    file.seek(0)
    print(file.read())
    