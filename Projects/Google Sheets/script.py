import gspread

grades_to_points = {
    "U": 0,
    "E3": 1,
    "E2": 2,
    "E1": 3,
    "D3": 4,
    "D2": 5,
    "D1": 6,
    "C3": 7,
    "C2": 8,
    "C1": 9,
    "B3": 10,
    "B2": 11,
    "B1": 12,
    "A3": 13,
    "A2": 14,
    "A1": 15,
    "A*3": 16,
    "A*2": 17,
    "A*1": 18,
}

sa = gspread.service_account()
sh = sa.open("GCSE")
wks = sh.worksheet("PPGs")


# -------------------------------------------- #


class Person:
    def __init__(self, name: str, start_row: int, end_row: int):
        self.name = name
        self.start_row = start_row
        self.end_row = end_row

    def __repr__(self):
        return f"Person({self.name}, {self.start_row}, {self.end_row})"

    def __str__(self):
        return self.name

    def get_subjects_list(self):
        subjects_list = []
        for i in range(self.start_row + 1, self.end_row + 1):
            subject = wks.cell(i, 1).value

            if subject == "":
                continue

            subjects_list.append(subject)

        return subjects_list

    def get_average_grade_for_subject(
        self,
        subject_row_num,
    ) -> dict[str, str] | None:
        subject_ppg = list(wks.get(f"C{subject_row_num}:J{subject_row_num}"))

        if subject_ppg == []:
            return None
        else:
            subject_ppg = subject_ppg[0]

        total_points = 0
        for i in subject_ppg:
            total_points += grades_to_points[i]

        average_points = round(total_points / len(subject_ppg))

        average_grade = list(grades_to_points.keys())[
            list(grades_to_points.values()).index(average_points)
        ]

        return {wks.cell(subject_row_num, 1).value: average_grade}

    def store_all_subjects_average_grades(self):

        for i in range(self.start_row + 1, self.end_row + 1):
            subject_average_grade = self.get_average_grade_for_subject(i)

            if subject_average_grade == None:
                continue

            wks.update_cell(i, 11, subject_average_grade[wks.cell(i, 1).value])


def get_total_subjects_average_grade(person_list: list[Person]):

    all_subjects_avg_grade_dict: dict[Person, dict[str, str]] = {}
    # Type : {Person: {Subject: Average Grade}}
    for person in person_list:
        subject_ppg_dict: dict[str, str] = {}
        for i in range(person.start_row + 1, person.end_row + 1):

            subject_max_grade: dict[
                str, str
            ] | None = person.get_average_grade_for_subject(i)

            if subject_max_grade == None:
                continue

            subject_ppg_dict.update(subject_max_grade)
        all_subjects_avg_grade_dict.update({person: subject_ppg_dict})

    # Now we go through this dict and find the max grade for each subject

    avg_grades_per_subject: dict[str, dict[str, str]] = {}
    # Type : {Subject: {Person.name: Average Grade}}
    # The difference between this and all_subjects_avg_grade_dict is that the nested
    # dict in this only contains one item
    for person in all_subjects_avg_grade_dict:
        for subject in all_subjects_avg_grade_dict[person]:
            if subject in avg_grades_per_subject:
                subject_grade_points = grades_to_points[
                    all_subjects_avg_grade_dict[person][subject]
                ]
                max_grade_points = 0
                try:
                    max_grade_points = grades_to_points[
                        avg_grades_per_subject[subject][person.name]
                    ]
                except KeyError:
                    original_persons_names = list(
                        avg_grades_per_subject[subject].keys()
                    )[0]
                    max_grade_points = grades_to_points[
                        avg_grades_per_subject[subject][original_persons_names]
                    ]
                finally:

                    if subject_grade_points > max_grade_points:
                        avg_grades_per_subject[subject].clear()
                        avg_grades_per_subject[subject].update(
                            {person.name: all_subjects_avg_grade_dict[person][subject]}
                        )

                    if subject_grade_points == max_grade_points:
                        original_persons_names = list(
                            avg_grades_per_subject[subject].keys()
                        )[0]
                        avg_grades_per_subject[subject].clear()
                        avg_grades_per_subject[subject].update(
                            {
                                f"{original_persons_names}, {person.name}": all_subjects_avg_grade_dict[
                                    person
                                ][
                                    subject
                                ]
                            }
                        )

            else:
                avg_grades_per_subject.update(
                    {
                        subject: {
                            person.name: all_subjects_avg_grade_dict[person][subject]
                        }
                    }
                )

    return avg_grades_per_subject


def store_total_subjects_max_grade(total_subjects_max_grade: dict[str, dict[str, str]]):
    for i, subject in enumerate(total_subjects_max_grade.keys()):
        wks.update(f"M{i + 2}", subject)

        wks.update(f"N{i + 2}", list(total_subjects_max_grade[subject].keys())[0])

        wks.update(f"O{i + 2}", list(total_subjects_max_grade[subject].values())[0])


if __name__ == "__main__":
    print(f"Number of rows: {wks.row_count}")
    print(f"Number of columns: {wks.col_count}")

    a_m = Person("A M", 1, 11)
    i_a = Person("I A", 14, 24)
    d_i = Person("D I", 26, 36)

    store_total_subjects_max_grade(get_total_subjects_average_grade([a_m, i_a, d_i]))
