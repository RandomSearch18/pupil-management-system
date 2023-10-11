import bcrypt
import hashlib
import json
from base64 import b64decode, b64encode
from pathlib import Path
from typing import Any, Callable, Optional


def check_password(inputted_password: str, correct_password_hash: str):
    # This is where we add `return true` https://youtu.be/y4GB_NDU43Q?t=97
    correct_hash_bytes = b64decode(correct_password_hash)
    processed_attempt = b64encode(
        hashlib.sha256(inputted_password.encode("utf-8")).digest()
    )

    return bcrypt.checkpw(processed_attempt, correct_hash_bytes)


def process_password(raw_password: str) -> bytes:
    """Returns a base64-encoded sha256 hash of the provided password string,
    so that it can then be hashed using bcrypt without its character limit being an issue.
    See https://pypi.org/project/bcrypt#maximum-password-length for details.
    """
    return b64encode(hashlib.sha256(raw_password.encode("utf-8")).digest())


class JSONDatabase:
    # By default, store data in the current directory
    base_path = Path(".")

    def save(self):
        """Saves the database to disk, overwriting that the file contents to match the in-memory data."""
        with open(self.file_path, "w") as file:
            json.dump(self.data, file)

    def load(self):
        """Loads the contents of the database file into memory, so that the data can be accessed."""
        with open(self.file_path, "r") as file:
            self.data = json.load(file)

    def get_initial_data(self, initial_data: Any, initial_data_filename: Optional[str]):
        """Checks the provided file for initial data, otherwise returns the fallback data.

        - initial_data_filename= is a filename (relative to the base path) of a file that contains default data for the database
        - This data will be used to initialise the database, if the argument is provided and the file exists
        - initial_data= is the fallback data, which will initialise the database if the above fails
        """
        if not initial_data_filename:
            return initial_data

        initial_data_path = Path(self.base_path, initial_data_filename)
        try:
            with open(initial_data_path, "r", encoding="utf-8") as initial_data_file:
                return json.load(initial_data_file)
        except FileNotFoundError:
            return initial_data

    def __init__(
        self,
        filename: str,
        initial_data: Any,
        initial_data_filename: Optional[str] = None,
    ):
        self.file_path = Path(self.base_path, filename)

        # Start off by reading the existing data from the file
        # (and if the file diesn't exist, initialise it with the provided initial data)
        try:
            self.load()
        except FileNotFoundError:
            self.data = self.get_initial_data(initial_data, initial_data_filename)
            self.save()


def get_file(file_path: Path, mode="r"):
    """Gets a file handle for the provided file path,
    creating the file if it doesn't already exist.
    Uses the provided mode argument, or defaults to read-only
    """
    try:
        return open(file_path, mode)
    except FileNotFoundError:
        # Create the file
        file = open(file_path, "w")
        file.close()

        return open(file_path, mode)
