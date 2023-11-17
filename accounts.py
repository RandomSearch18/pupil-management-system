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
