"""Mr Leeman's System: A pupil management system for Tree Road School
This code is for Task 3 of the lesson 2.2.1 Programming fundamentals - validation"""

from colorama import Style
from colorama import init as init_colorama

import inputs
from accounts import AccountsDatabase
from menu import Menu, Option, Submenu, bold, color, error_incorrect_input, print_hint, info_line
from students import StudentsDatabase


def log_in():
    target_username = inputs.text("Username: ", "Enter your username")
    matching_user = accounts_database.get_account(username=target_username)

    if not matching_user:
        error_incorrect_input(
            f"No account exists with the username {bold(target_username)}")
        return log_in()

    is_authenticated = accounts_database.authenticate_user(target_username)
    if not is_authenticated:
        return

    # From this point on, our user is authenticated
    global current_account
    current_account = matching_user


def ask_for_new_username(show_tip=True) -> str:
    username = inputs.new_username("Create a username: ")

    matching_user = accounts_database.get_account(username)
    if matching_user:
        error_incorrect_input(
            f"There's already an account with the username {bold(username)}")
        if show_tip:
            print_hint("Tip: Pick another username or try logging in instead.")

        return ask_for_new_username(show_tip=False)

    return username


def create_account():
    print_hint(
        "Your username will identify you as an individual, and you'll enter it to access this system."
    )
    username = ask_for_new_username()

    print_hint(
        "Your password is a secret phrase that you'll use to prove who you are when you log in."
        + " It cannot be reset, so keep it safe!")
    print_hint(
        "Note: You won't be able to see your password while you're typing it.")
    password_hash = inputs.new_password("Set your password: ")

    accounts_database.add_account(username, password_hash)
    print()
    print(f"Created a new account called {bold(username)}")


def register_student():
    """Asks the user to input the data for a new student
    
    - Doesn't ask for email or ID as those are generated
    - Adds the student to the database"""
    forename = inputs.name("Forename: ")
    surname = inputs.name("Surname: ")
    birthday = inputs.date(f"Birthday: {color('(YYYY-MM-DD)', Style.DIM)} ")
    tutor_group = inputs.tutor_group("Tutor group: ")
    home_address = inputs.multiline("Home address: ")
    home_phone = inputs.phone_number("Home phone number: ")

    student = students_database.add_student(surname, forename, birthday,
                                            home_address, home_phone,
                                            tutor_group)

    # Print the details that we generated
    print()
    print(
        f"Registered student {bold(student['full_name'])} (ID #{student['id']})"
    )
    info_line("School email address", student['school_email'])
    info_line("ID number", student['id'])


def log_out():
    global current_account
    if not current_account:
        return print("Nobody is signed in!")

    old_username = current_account["username"]
    current_account = None
    print(f"Logged out of account {bold(old_username)}")


# Initialise the Colorama libary for terminal formatting utils
init_colorama()

# Initialise the JSON databases
accounts_database = AccountsDatabase()
students_database = StudentsDatabase()

current_account = None  # Store the account that is currently signed in

main_menu = Menu(
    title="Mr Leeman's system",
    options=[
        Option("Log in", log_in, lambda: not current_account),
        Option("Create account", create_account, lambda: not current_account),
        Option("Register new student", register_student,
               lambda: bool(current_account)),
        Option("Log out", log_out, lambda: bool(current_account)),
        Submenu("Go to the sub menu", "Sub-menu",
                [Option("Log in 1", log_in),
                 Option("Log in 2", log_in)])
    ],
)

main_menu.show(loop=True)
