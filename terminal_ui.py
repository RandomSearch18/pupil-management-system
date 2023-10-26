"""The main code for the menu-driven, text-based interface."""

from typing import Callable
from colorama import Style
from colorama import init as init_colorama
from app import App

import inputs
from menu import (
    Menu,
    Option,
    bold,
    clear_screen,
    color,
    error_incorrect_input,
    info_line,
    print_hint,
    wait_for_enter_key,
)
from reports import ReportsMenu


# def page(pause_at_end = True, clear_at_start = True):
#     """Pages are sections of the UI for viewing inforomation or perfoming an action"""
#     def make_page(callback: Callable[[], None]):
#         def wrapper(self):
#             #print(self.log_in)
#             if clear_at_start:
#                 #clear_screen()
#                 print("Clear")
#             print(callback)
#             #callback()
#             if pause_at_end:
#                 wait_for_enter_key()
#         return wrapper
#     return make_page

def page(pause_at_end = True, clear_at_start = True):
    def make_page(callback):
        def wrapper(self):
            if clear_at_start:
                clear_screen()
            
            result = 1
            while isinstance(result, int) and result > 0:
                # The callback returned a positive number, so it wants to be restarted
                result = callback(self)

            if pause_at_end:
                print()
                wait_for_enter_key()
        return wrapper
    return make_page

class TerminalUI:
    """A friendly, cross-platform interface to the pupil management system that runs in the terminal"""

    def __init__(self, app: App) -> None:
        self.app = app

    def page(pause_at_end = True, clear_at_start = True):
        def make_page(callback):
            def wrapper(self):
                if clear_at_start:
                    clear_screen()
                
                result = 1
                while isinstance(result, int) and result > 0:
                    # The callback returned a positive number, so it wants to be restarted
                    result = callback(self)

                if pause_at_end:
                    print()
                    wait_for_enter_key()
            return wrapper
        return make_page
    
    @page(pause_at_end=False)
    def log_in(self):
        target_username = inputs.text("Username: ", "Enter your username")
        matching_user = self.app.accounts_database.get_account(username=target_username)

        if not matching_user:
            error_incorrect_input(
                f"No account exists with the username {bold(target_username)}"
            )
            return 1

        is_authenticated = self.app.accounts_database.authenticate_user(target_username)
        if not is_authenticated:
            return

        # From this point on, our user is authenticated
        self.app.current_account = matching_user

    def ask_for_new_username(self, show_tip=True) -> str:
        username = inputs.new_username("Create a username: ")

        matching_user = self.app.accounts_database.get_account(username)
        if matching_user:
            error_incorrect_input(
                f"There's already an account with the username {bold(username)}"
            )
            if show_tip:
                print_hint("Tip: Pick another username or try logging in instead.")

            return self.ask_for_new_username(show_tip=False)

        return username

    @page()
    def create_account(self):
        print_hint(
            "Your username will identify you as an individual, and you'll enter it to access this system."
        )
        username = self.ask_for_new_username()

        print()

        print_hint(
            "Your password is a secret phrase that you'll use to prove who you are when you log in."
            + " It cannot be reset, so keep it safe!"
        )
        print_hint(
            "Note: You won't be able to see your password while you're typing it."
        )
        password_hash = inputs.new_password("Set your password: ")

        print()
        self.app.accounts_database.add_account(username, password_hash)
        print(f"Created a new account called {bold(username)}")

    @page()
    def register_student(self):
        """Asks the user to input the data for a new student

        - Doesn't ask for email or ID as those are generated
        - Adds the student to the database"""
        forename = inputs.name("Forename: ")
        surname = inputs.name("Surname: ")
        birthday = inputs.date(f"Birthday: {color('(YYYY-MM-DD)', Style.DIM)} ")
        tutor_group = inputs.tutor_group("Tutor group: ")
        home_address = inputs.multiline("Home address: ")
        home_phone = inputs.phone_number("Home phone number: ")

        student = self.app.students_database.add_student(
            surname, forename, birthday, home_address, home_phone, tutor_group
        )

        # Print the details that we generated
        print()
        print(f"Registered student {bold(student['full_name'])} (ID #{student['id']})")
        info_line("School email address", student["school_email"])
        info_line("ID number", student["id"])

    @page(clear_at_start=False)
    def log_out(self):
        if not self.app.signed_in():
            return print("Nobody is signed in!")

        old_username = self.app.current_account["username"]
        self.app.current_account = None
        print(f"Logged out of account {bold(old_username)}")

    @page()
    def show_student_info(self):
        print_hint(
            "Each student has a numerical ID that is used to uniquely identify them."
        )
        target_id = inputs.integer("Enter unique ID: ")

        matching_student = self.app.students_database.get_student(id=target_id)

        if not matching_student:
            error_incorrect_input(f"No students with the ID {bold(target_id)}")
            return self.show_student_info()

        print()
        self.app.students_database.display_student_info(matching_student)

    @page(pause_at_end=False)
    def view_reports(self):
        reports_menu = ReportsMenu(self.app.students_database.get_students())
        reports_menu.show()

    def show(self):
        """The entrypoint for the menu-based UI"""
        # Initialise the Colorama libary for terminal formatting utils
        init_colorama()

        main_menu = Menu(
            title="Mr Leeman's system",
            options=[
                Option(
                    "Log in",
                    self.log_in,
                    lambda: not self.app.signed_in()
                    and self.app.accounts_database.data,
                ),
                Option(
                    "Create account",
                    self.create_account,
                    lambda: not self.app.signed_in(),
                ),
                Option(
                    "Register new student",
                    self.register_student,
                    lambda: self.app.signed_in(),
                ),
                Option(
                    "Get a student's details",
                    self.show_student_info,
                    lambda: self.app.students_database.get_students(),
                ),
                Option(
                    "View student reports",
                    self.view_reports,
                    lambda: self.app.signed_in(),
                ),
                Option("Log out", self.log_out, lambda: self.app.signed_in()),
            ],
        )

        main_menu.show(loop=True)
