from typing import Callable
from colorama import Style
from menu import Menu, Option, bold, clear_screen, color
from datetime import date


def display_report(students: list[dict], title: str):
    """Prints the students in a report, with nice formatting"""
    clear_screen()
    print(bold(title))
    print()
    
    for i, student in enumerate(students):
        index = i + 1
        index_part = color(f"{index:3})", Style.DIM)
        name_part = student["full_name"]
        print(f"{index_part} {name_part}")
    
    print()
    input(color("Press Enter to continue...", Style.DIM))


def birthday_this_month(student):
    """Checks if the provided student's birthday is this month"""
    birthday = date.fromisoformat(student["birthday"])
    return birthday.month == date.today().month


class ReportsMenu:
    def __init__(self, students: list[dict]):
        self.students = students

    def generate_and_show_report(
        self, filter_callback: Callable[[dict], bool], title: str
    ):
        chosen_students = filter(filter_callback, self.students)
        display_report(chosen_students, title)

    def report_option(
        self, title: str, filter_callback: Callable[[dict], bool], description: str
    ):
        return Option(
            title,
            lambda: self.generate_and_show_report(filter_callback, title),
            description=description,
        )

    def show(self):
        menu = Menu(
            [
                self.report_option(
                    "Birthdays this month",
                    birthday_this_month,
                    description="TODO: Write explanation",
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
