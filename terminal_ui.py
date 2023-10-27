"""The main code for the menu-driven, text-based interface."""

from typing import Callable, Optional
from colorama import Style
from colorama import init as init_colorama
from app import App

import inputs
from menu import (
    Menu,
    Page,
    bold,
    clear_screen,
    color,
    error_incorrect_input,
    info_line,
    print_hint,
    wait_for_enter_key,
)
from reports import ReportsMenu


class Breadcrumbs:
    """Keeps track of the hierarchy of pages being viewed by the user"""

    def __init__(self):
        self.pages = []

    def push(self, page: str) -> int:
        """Adds a page onto the end of the breadcrumbs

        - Represents a foreward navigation action
        - Returns the index of the added page
        """
        self.pages.append(page)
        return len(self.pages) - 1

    def pop(self):
        """Removes the page at the end of the breadcrumbs

        - Represents a backward navigation action
        """
        self.pages.pop()
        # TODO Maybe this should return the index of the removed item or something

    def replace(self, page: str):
        """Replaces the page at the end of the breadcrumbs with the provided page

        - Represents a sideways navigation action
        - Retuns the index of the new (replaced) page
        """
        self.pages[-1] = page
        return len(self.pages) - 1

    def to_formatted(self):
        """Generates a nicely-formatted line of text from the breadcrumbs"""
        formatted_pages = [bold(page) for page in self.pages]
        pretty_breadcrumbs = " > ".join(formatted_pages)
        return pretty_breadcrumbs 


class TerminalUI:
    """A friendly, cross-platform interface to the pupil management system that runs in the terminal"""

    def __init__(self, app: App) -> None:
        self.app = app
        self.breadcrumbs = Breadcrumbs()

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

    def log_out(self):
        if not self.app.signed_in():
            return print("Nobody is signed in!")

        old_username = self.app.current_account["username"]
        self.app.current_account = None
        print(f"Logged out of account {bold(old_username)}")

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

    def view_reports(self):
        reports_menu = ReportsMenu(self.app, ui=self)
        reports_menu.show()

    def show(self):
        """The entrypoint for the menu-based UI"""
        # Initialise the Colorama libary for terminal formatting utils
        init_colorama()

        self.breadcrumbs.push(self.app.brand.APP_NAME)

        options = [
            Page(
                "Log in",
                self.log_in,
                lambda: not self.app.signed_in() and self.app.accounts_database.data,
                pause_at_end=False,
            ),
            Page(
                "Create account",
                self.create_account,
                lambda: not self.app.signed_in(),
            ),
            Page(
                "Register new student",
                self.register_student,
                lambda: self.app.signed_in(),
            ),
            Page(
                "Get a student's details",
                self.show_student_info,
                lambda: self.app.students_database.get_students(),
            ),
            Page(
                "View student reports",
                self.view_reports,
                lambda: self.app.signed_in(),
                pause_at_end=False
            ),
            Page(
                "Log out",
                self.log_out,
                lambda: self.app.signed_in(),
                clear_at_start=False,
            ),
        ]

        main_menu = Menu(
            options=options,
            ui=self
        )

        main_menu.show(loop=True)
