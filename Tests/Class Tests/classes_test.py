import pytest


grades = {
    "A1": 100,
    "A2": 95,
    "A3": 90,
    "B1": 85,
    "B2": 80,
    "B3": 75,
    "C1": 70,
    "C2": 65,
    "C3": 60,
    "D1": 55,
    "D2": 50,
    "D3": 45,
    "E1": 40,
    "E2": 35,
    "E3": 30,
    "F1": 25,
    "F2": 20,
    "F3": 15,
    "G1": 10,
    "G2": 5,
    "G3": 0,
}


class Student:
    def __init__(self, name, age, grade, attendance):
        self.name = name
        self.age = age
        self.grade = grade
        self.attendance = attendance

    def get_grade(self):
        return self.grade

    def get_attendance(self):
        return str(self.attendance) + "%"


class English(Student):
    def __init__(self, name, age, grade, attendance=90):
        super().__init__(name, age, grade, attendance)


bob = English("Bob", 14, "A1", 75)
tim = English("Tim", 14, "C3", 35)
jeffery = English("Jeffery", 16, "B1")


def get_max_grade(*students):
    numerical_grade = [grades[students[i].get_grade()] for i in range(len(students))]
    max_grade = max(numerical_grade)
    student_with_max_grade = [
        students[i].name
        for i in range(len(students))
        if grades[students[i].get_grade()] == max_grade
    ]
    return str(student_with_max_grade)


def test_get_max_grade():
    assert get_max_grade(bob, jeffery, tim).strip("[]").strip("''") == "Bob"
