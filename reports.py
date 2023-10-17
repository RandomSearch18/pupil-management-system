from typing import Callable
from colorama import Style
from inputs import text
from menu import Menu, Option, bold, clear_screen, color, wait_for_enter_key
from datetime import date

from util import iso_to_locale_string


def print_report_item(index: int, main_text: str, *suffixes: str):
    one_indexed_index = index + 1
    index_part = color(f"{one_indexed_index:3})", Style.DIM)

    suffix_part = color(" ".join(suffixes), Style.DIM) if suffixes else ""
    print(" ".join([index_part, main_text, suffix_part]))


def upcoming_birthdays(students: list[dict]):
    """A report of students' birthdays in the next 30 days"""
    target_students = []
    for student in students:
        birthday = date.fromisoformat(student["birthday"])
        birthday_this_year = birthday.replace(year=date.today().year)

        time_until_birthday = birthday_this_year - date.today()
        # Lower bound of 0 to ensure birthday hasn't already passed
        birthday_is_soon = 0 <= time_until_birthday.days <= 30
        if birthday_is_soon:
            target_students.append(student)

    for i, student in enumerate(target_students):
        birthday_string = iso_to_locale_string(student["birthday"])
        print_report_item(i, birthday_string, student["full_name"])


def surnames_starting_with(students: list[dict]):
    target_substring = text(f"Include surnames that start with: ").lower()

    target_students = []
    for student in students:
        surname_matches = student["surname"].lower().startswith(target_substring)
        if surname_matches:
            target_students.append(student)
    
    for i, student in enumerate(target_students):
        formatted_name = ", ".join([student["surname"], student["forename"]])
        print_report_item(i, formatted_name)



class ReportsMenu:
    def __init__(self, students: list[dict]):
        self.students = students

    def report_option(
        self,
        title: str,
        show_report: Callable[[list[dict]], None],
        description: str,
    ):
        def callback():
            clear_screen()
            print(f"{bold('Reports')} > {bold(title)}")
            print()
            show_report(self.students)
            print()
            wait_for_enter_key()

        return Option(
            title,
            callback,
            description=description,
        )

    def show(self):
        menu = Menu(
            [
                self.report_option(
                    "Upcoming birthdays",
                    upcoming_birthdays,
                    description="A list of students whose birthdays are in the next 30 days. "
                    + "This can be used to add upcoming birthdays to a noticeboard, or simply wish your students a happy birthday.",
                ),
                self.report_option(
                    "Surnames starting with...",
                    surnames_starting_with,
                    description="Lists students in alphabetica",
                ),
            ],
            "Choose a report to view",
        )
        menu.show()
