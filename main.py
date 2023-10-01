"""Mr Leeman's System: A pupil management system for Tree Road School
This code is for Task 3 of the lesson 2.2.1 Programming fundamentals - validation"""

import hashlib

from colorama import Fore, Style
from colorama import init as init_colorama

import inputs
from menu import Menu, Option, Submenu
from util import JSONDatabase, check_password


def log_in():
    account = accounts[0]

    attempt = inputs.password("Password: ")
    is_authenticated = check_password(attempt, account["password_hash"])
    print(is_authenticated)


def create_account():
    print(
        "Your username will identify you as an individual, and you'll enter it to access this system."
    )
    username = inputs.username("Create a username: ")

    # TODO: Check for dupe usernames

    print(
        "Your password is a secret phrase that you'll use to prove who you are when you log in"
    )
    print(
        "Note that you won't be able to see your password while you're entering it"
    )
    password_hash = inputs.new_password("Set your password: ")

    accounts.append({"username": username, "password_hash": password_hash})
    accounts_database.save()
    print()
    print(
        f"Created a new account called {Style.BRIGHT}{username}{Style.RESET_ALL}"
    )


init_colorama()
accounts_database = JSONDatabase("accounts.json", [])
accounts = accounts_database.data

current_account = None

main_menu = Menu(
    title="Mr Leeman's system",
    options=[
        Option("Log in", log_in, lambda: not current_account),
        Option("Create account", create_account),
        Submenu("Go to the sub menu", "Sub-menu",
                [Option("Log in 1", log_in),
                 Option("Log in 2", log_in)])
    ],
)

main_menu.show(loop=True)
