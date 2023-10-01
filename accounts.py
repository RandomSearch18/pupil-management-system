import inputs
from util import JSONDatabase, check_password


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

    def authenticate_user(self, username: str) -> bool:
        """Prompts the user to enter their password, in order to log in with the provided username.
        Keeps prompting for a password until it's correctly entered or the user cancels.
        Returns True if authentication was successful, and False if it wasn't.
        Warning: The user has not been authenticated if the function returns False. Ensure this case is handled accordingly.
        """
        user = self.get_user(username)
        if not user:
            raise LookupError(f"User doesn't exist: {username}")
        correct_password_hash = user["password_hash"]

        try:
            attempt = inputs.password("Password: ")
        except KeyboardInterrupt:
            return False

        is_authenticated = check_password(attempt, correct_password_hash)
        if is_authenticated: return True

        return self.authenticate_user(username)
