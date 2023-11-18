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
