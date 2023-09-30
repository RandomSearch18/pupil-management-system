"""Mr Leeman's System: A pupil management system for Tree Road School
This code is for Task 3 of the lesson 2.2.1 Programming fundamentals - validation"""

from menu import Menu, Option, Submenu
from util import JSONDatabase


def log_in():
    print("Logging in")
    print(accounts_database.data)
    input()


accounts_database = JSONDatabase("accounts.json", [])

main_menu = Menu(
    title="Mr Leeman's system",
    options=[
        Option("Log in", log_in),
        Submenu("Go to the sub menu", "Sub-menu",
                [Option("Log in 1", log_in),
                 Option("Log in 2", log_in)])
    ],
)

main_menu.show(loop=True)
