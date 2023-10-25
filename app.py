"""Manages the global context for the app, serving as a back-end for database access etc."""

from accounts import AccountsDatabase
from settings import SettingsDatabase
from students import StudentsDatabase


class App:
    """A running instance of the application"""

    def __init__(self) -> None:
        # Initialise the JSON databases
        self.settings_database = SettingsDatabase()
        self.accounts_database = AccountsDatabase()
        self.students_database = StudentsDatabase()

        # Store the account that is currently signed in
        self.current_account = None