from typing import Callable
from colorama import Style
from menu import Menu, Option, bold, clear_screen, color, wait_for_enter_key
from datetime import date

from util import iso_to_locale_string


def display_report(
    students: list[dict], title: str, suffixes: list[Callable[[dict], str]]
):
    """Prints the students in a report, with nice formatting"""
    clear_screen()
    print(bold(title))
    print()

    for i, student in enumerate(students):
        index = i + 1
        index_part = color(f"{index:3})", Style.DIM)
        name_part = student["full_name"]

        suffix = [callback(student) for callback in suffixes]
        suffix_part = color(" ".join(suffix), Style.DIM) if suffix else ""

        print(" ".join([index_part, name_part, suffix_part]))

    print()
    wait_for_enter_key()


def upcoming_birthday(student):
    """Checks if the provided student's birthday is coming up in the next 30 days"""
    birthday = date.fromisoformat(student["birthday"])
    birthday_this_year = birthday.replace(year=date.today().year)

    time_until_birthday = birthday_this_year - date.today()
    # Lower bound to ensure birthday hasn't already passed
    return 0 <= time_until_birthday.days <= 30


class ReportsMenu:
    def __init__(self, students: list[dict]):
        self.students = students

    def generate_and_show_report(
        self,
        filter_callback: Callable[[dict], bool],
        title: str,
        suffixes: list[Callable[[dict], str]],
    ):
        chosen_students = filter(filter_callback, self.students)
        display_report(chosen_students, title, suffixes)

    def report_option(
        self,
        title: str,
        filter_callback: Callable[[dict], bool],
        description: str,
        suffixes: list[Callable[[dict], str]] = [],
    ):
        return Option(
            title,
            lambda: self.generate_and_show_report(filter_callback, title, suffixes),
            description=description,
        )

    def show(self):
        menu = Menu(
            [
                self.report_option(
                    "Upcoming birthdays",
                    upcoming_birthday,
                    suffixes=[
                        lambda student: f"({iso_to_locale_string(student['birthday'])})"
                    ],
                    description="A list of students whose birthdays are in the next 30 days. "
                    + "This can be used to add upcoming birthdays to a noticeboard, or simply wish your students a happy birthday.",
                ),
                Option(
                    "Alphabetical order",
                    input,
                    description="TODO: Write another explanation!",
                ),
            ],
            "Choose a report to view",
        )
        menu.show()
