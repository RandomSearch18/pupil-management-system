from typing import Optional
from colorama import Style

import inputs
from menu import color, error_incorrect_input, print_hint
from util import JSONDatabase, check_password


class AccountsDatabase(JSONDatabase):

    def __init__(self):
        super().__init__("accounts.json", [])

    def get_account(self, username: str) -> Optional[dict]:
        for account in self.data:
            if username and account["username"] == username:
                return account
        return None

    def get_usernames(self) -> list[str]:
        return [account["username"] for account in self.data]

    def add_account(self, username: str, password_hash: str):
        normalised_username = username.lower()
        if self.get_account(normalised_username):
            raise ValueError(f"Username {normalised_username} already exists")

        new_account = {"username": normalised_username, "password_hash": password_hash}
        self.data.append(new_account)
        self.save()

    def authenticate_user(self, username: str, suppress_hints=False) -> bool:
        """Prompts the user to enter their password, in order to log in with the provided username.
        Keeps prompting for a password until it's correctly entered or the user cancels.
        Returns True if authentication was successful, and False if it wasn't.
        Warning: The user has not been authenticated if the function returns False. Ensure this case is handled accordingly.
        """
        user = self.get_account(username)
        if not user:
            raise LookupError(f"User doesn't exist: {username}")
        correct_password_hash = user["password_hash"]

        try:
            attempt = inputs.password("Password: ")
        except KeyboardInterrupt:
            return False

        is_authenticated = check_password(attempt, correct_password_hash)
        if is_authenticated: return True

        error_incorrect_input("Incorrect password")
        if not suppress_hints:
            # Let the user know how to give up entering their password
            print_hint("Tip: Try again or press Ctrl+C to cancel")
        return self.authenticate_user(username, suppress_hints=True)
