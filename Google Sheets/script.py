import gspread

grades_to_points = {
    "U": 0,
    "C3": 1,
    "C2": 2,
    "C1": 3,
    "B3": 4,
    "B2": 5,
    "B1": 6,
    "A3": 7,
    "A2": 8,
    "A1": 9,
    "A*3": 10,
    "A*2": 11,
    "A*1": 12,
}

sa = gspread.service_account()
sh = sa.open("GCSE")
wks = sh.worksheet("PPGs")

print(f"Number of rows: {wks.row_count}")
print(f"Number of columns: {wks.col_count}")


def person_averages_finder(start_row, end_row):

    for i in range(start_row, end_row + 1):

        if list(wks.get(f"C{i}:J{i}")) == []:
            # If the cell is empty, skip the row
            continue

        subject_ppg = list(wks.get(f"C{i}:J{i}"))[0]

        total_points = 0

        for j in subject_ppg:
            total_points += grades_to_points[j]

        average_points = round(total_points / len(subject_ppg))

        average_grade = list(grades_to_points.keys())[
            list(grades_to_points.values()).index(average_points)
        ]

        wks.update(f"K{i}", average_grade)


person_averages_finder(2, 11)
person_averages_finder(15, 24)
