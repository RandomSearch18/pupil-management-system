"""The main code for the menu-driven, text-based interface."""

from typing import Callable, Optional
from colorama import Fore, Style
from colorama import init as init_colorama
from app import App

from inputs import Inputs
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
from onboarding import Onboarding
from reports import ReportsMenu
from ui import UI
from util import check_password


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
        formatted_pages = []
        for i, page in enumerate(self.pages):
            is_active_page = i == len(self.pages) - 1
            formatted_page = (
                bold(page) if is_active_page else color(page, Style.DIM + Style.BRIGHT)
            )
            formatted_pages.append(formatted_page)

        pretty_breadcrumbs = " > ".join(formatted_pages)
        return pretty_breadcrumbs


class TerminalUI(UI):
    """A friendly, cross-platform interface to the pupil management system that runs in the terminal"""

    def __init__(self, app: App) -> None:
        inputs = Inputs()
        super().__init__(inputs, app)

        self.breadcrumbs = Breadcrumbs()
        self.inputs = Inputs()

    def user_authentication(self, username, suppress_hints=False):
        """Prompts the user to enter their password, in order to log in with the provided username.

        Keeps prompting for a password until it's correctly entered or the user cancels.
        Returns True if authentication was successful, and False if it wasn't.
        Warning: The user has not been authenticated if the function returns False. Ensure this case is handled accordingly.
        """
        user = self.app.accounts_database.get_account(username)
        if not user:
            raise LookupError(f"User doesn't exist: {username}")
        correct_password_hash = user["password_hash"]

        try:
            attempt = self.inputs.password("Password: ")
        except KeyboardInterrupt:
            return False

        is_authenticated = check_password(attempt, correct_password_hash)
        if is_authenticated:
            return True

        error_incorrect_input("Incorrect password")
        if not suppress_hints:
            # Let the user know how to give up entering their password
            print_hint("Tip: Try again or press Ctrl+C to cancel")
        return self.authenticate_user(username, suppress_hints=True)

    def log_in(self):
        target_username = self.inputs.text("Username: ", "Enter your username")
        matching_user = self.app.accounts_database.get_account(username=target_username)

        if not matching_user:
            error_incorrect_input(
                f"No account exists with the username {bold(target_username)}"
            )
            return 1

        is_authenticated = self.user_authentication(target_username)
        if not is_authenticated:
            return

        # From this point on, our user is authenticated
        self.app.current_account = matching_user

    def ask_for_new_username(self, show_tip=True) -> str:
        username = self.inputs.new_username("Create a username: ")

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
        print_hint("Usernames should be easy to type and unique to yourself.")
        username = self.ask_for_new_username()
        print()

        print_hint("Passwords cannot be reset - keep it safe!")
        print_hint(
            "Note: You won't be able to see your password while you're typing it."
        )
        password_hash = self.inputs.new_password("Set your password: ")

        print()
        self.app.accounts_database.add_account(username, password_hash)
        print(f"Created a new account called {bold(username)}")

    def register_student(self):
        """Asks the user to input the data for a new student

        - Doesn't ask for email or ID as those are generated
        - Adds the student to the database"""
        forename = self.inputs.name("Forename: ")
        surname = self.inputs.name("Surname: ")
        birthday = self.inputs.date(f"Birthday: {color('(YYYY-MM-DD)', Style.DIM)} ")
        tutor_group = self.inputs.tutor_group("Tutor group: ")
        home_address = self.inputs.multiline("Home address: ")
        home_phone = self.inputs.phone_number("Home phone number: ")

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
        target_id = self.inputs.integer("Enter unique ID: ")

        matching_student = self.app.students_database.get_student(id=target_id)

        if not matching_student:
            error_incorrect_input(f"No students with the ID {bold(target_id)}")
            return self.show_student_info()

        print()
        self.app.students_database.display_student_info(matching_student)

    def view_reports(self):
        reports_menu = ReportsMenu(self.app, ui=self)
        reports_menu.show()

    def trigger_exception(self):
        raise RuntimeError("Manually-triggered exception for debug purposes")

    def show(self):
        """The entrypoint for the menu-based UI"""
        # Initialise the Colorama libary for terminal formatting utils
        init_colorama()

        self.breadcrumbs.push(self.app.brand.APP_NAME)

        # Enter onboarding on first run (or if onboarding was left unfinished last time)
        if self.app.settings_database.get("tui", "onboarding", "show"):
            try:
                Onboarding(app=self.app, ui=self).show()
            except KeyboardInterrupt:
                # Exit the terminal UI
                return

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
                pause_at_end=False,
            ),
            Page(
                "Log out",
                self.log_out,
                lambda: self.app.signed_in(),
                clear_at_start=False,
            ),
            # Page("Debug: Trigger an exception", self.trigger_exception),
        ]

        main_menu = Menu(options=options, ui=self)

        main_menu.show(loop=True)
