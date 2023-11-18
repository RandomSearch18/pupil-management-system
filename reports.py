from __future__ import annotations
from typing import Callable, TYPE_CHECKING
from colorama import Style
from app import App
from menu import Menu, Page, bold, clear_screen, color
from datetime import date

if TYPE_CHECKING:
    from terminal_ui import TerminalUI

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
    """Asks for a letter and prints a report of students with a surname beginning with it"""
    target_substring = text("Include surnames that start with: ").lower()

    # Case-insensitively get students whose surname startw with the inputted string
    target_students = []
    for student in students:
        surname_matches = student["surname"].lower().startswith(target_substring)
        if surname_matches:
            target_students.append(student)

    # Sort alphabetically by surname
    target_students.sort(key=lambda student: student["surname"])

    # Print students' names in the format "Surname, Forename", since we're sorting by surname
    for i, student in enumerate(target_students):
        formatted_name = ", ".join([student["surname"], student["forename"]])
        print_report_item(i, formatted_name)


def forenames_starting_with(students: list[dict]):
    """Asks for a letter and prints a report of students with a forename beginning with it"""
    target_substring = text("Include forenames that start with: ").lower()

    # Case-insensitively get students whose forename startw with the inputted string
    target_students = []
    for student in students:
        forename_matches = student["forename"].lower().startswith(target_substring)
        if forename_matches:
            target_students.append(student)

    # Sort alphabetically by forename
    target_students.sort(key=lambda student: student["forename"])

    # Print students' names in the format "Forename Surname", since we're sorting by forename
    for i, student in enumerate(target_students):
        formatted_name = " ".join([student["forename"], student["surname"]])
        print_report_item(i, formatted_name)


class ReportsMenu:
    def __init__(self, app: App, ui: TerminalUI):
        self.app = app
        self.ui = ui

    def report_option(
        self,
        title: str,
        show_report: Callable[[list[dict]], None],
        description: str,
    ):
        def show_report_wrapper():
            students = self.app.students_database.get_students()
            print()
            show_report(students)

        return Page(
            title,
            show_report_wrapper,
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
                    description="A list of students whose surnames begin with a letter you choose, sorted alphabetically. "
                    + "Can be used to decide who to let out of the classroom first, or as a last resort for taking the register.",
                ),
                self.report_option(
                    "Forenames starting with...",
                    forenames_starting_with,
                    description="A list of students whose forenames begin with a letter you choose, sorted alphabetically. "
                    + "Can be used as a more personal way to decide who to let out of the classroom first, or to find people with similar names that may accidentally be confused.",
                ),
            ],
            ui=self.ui,
        )
        menu.show()
