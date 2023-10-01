from util import JSONDatabase


class AccountsDatabase(JSONDatabase):

    def __init__(self):
        super().__init__("accounts.json", [])

    def get_user(self, username: str) -> dict | None:
        for account in self.data:
            if username and account["username"] == username:
                return account
        return None

    def add_user(self, username: str, password_hash: str):
        new_user = {"username": username, "password_hash": password_hash}
        self.data.append(new_user)
        self.save()
