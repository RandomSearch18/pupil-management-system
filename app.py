"""Manages the global context for the app, serving as a back-end for database access etc."""

from accounts import AccountsDatabase
from settings import SettingsDatabase
from students import StudentsDatabase


class Brand:
    """Contains branding and metadata for the app"""
    APP_NAME = "Mr Leeman's System"

class App:
    """A running instance of the application"""

    def __init__(self) -> None:
        self.brand = Brand

        # Initialise the JSON databases
        self.settings_database = SettingsDatabase()
        self.accounts_database = AccountsDatabase()
        self.students_database = StudentsDatabase(app=self)

        # Store the account that is currently signed in
        self.current_account = None

    def signed_in(self):
        """Checks if the user is signed in with an account"""
        return self.current_account is not None
