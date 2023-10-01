"""Mr Leeman's System: A pupil management system for Tree Road School
This code is for Task 3 of the lesson 2.2.1 Programming fundamentals - validation"""

import hashlib

from colorama import Style
from colorama import init as init_colorama

import inputs
from accounts import AccountsDatabase
from menu import Menu, Option, Submenu, error_incorrect_input
from util import check_password


def log_in():
    target_username = inputs.text("Username: ", "Enter your username")
    matching_user = accounts_database.get_user(username=target_username)

    if not matching_user:
        error_incorrect_input(
            f"No account exists with the username {target_username}.")
        return log_in()

    attempt = inputs.password("Password: ")
    is_authenticated = check_password(attempt, matching_user["password_hash"])
    print(is_authenticated)


def create_account():
    print(
        "Your username will identify you as an individual, and you'll enter it to access this system."
    )
    username = inputs.new_username("Create a username: ")

    matching_user = accounts_database.get_user(username)
    if matching_user:
        error_incorrect_input(
            f"There's already an account with the username {username}")
        print("To continue, pick another username or try logging in instead.")
        return create_account()

    print(
        "Your password is a secret phrase that you'll use to prove who you are when you log in"
    )
    print(
        "Note that you won't be able to see your password while you're entering it"
    )
    password_hash = inputs.new_password("Set your password: ")

    accounts_database.add_user(username, password_hash)
    accounts_database.save()
    print()
    print(
        f"Created a new account called {Style.BRIGHT}{username}{Style.RESET_ALL}"
    )


# Initialise the Colorama libary for terminal formatting utils
init_colorama()

accounts_database = AccountsDatabase()
current_account = None  # Store the account that is currently signed in

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
