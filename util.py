import bcrypt
import hashlib
import json
from base64 import b64decode, b64encode
from pathlib import Path
from typing import Any, Callable, Optional
from datetime import date


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
    def get_file_path(self):
        """Get the path to the database's JSON file"""
        return self.file_path

    def save(self):
        """Saves the database to disk, overwriting that the file contents to match the in-memory data."""
        with open(self.file_path, "w") as file:
            json.dump(self.data, file)

    def load(self):
        """Loads the contents of the database file into memory, so that the data can be accessed."""
        with open(self.file_path, "r") as file:
            self.data = json.load(file)

    def get_initial_data(self, initial_data: Any, initial_data_path: Optional[Path]):
        """Checks the provided file for initial data, otherwise returns the fallback data.

        - initial_data_path= is the path to a file that contains default data for the database
        - This data will be used to initialise the database, if the argument is provided and the file exists
        - initial_data= is the fallback data, which will initialise the database if the above fails
        """
        if not initial_data_path:
            return initial_data

        try:
            with open(initial_data_path, "r", encoding="utf-8") as initial_data_file:
                return json.load(initial_data_file)
        except FileNotFoundError:
            return initial_data

    def __init__(
        self,
        filename: str,
        initial_data: Any,
        initial_data_path: Optional[Path] = None,
    ):
        if not hasattr(self, "base_path"):
            raise RuntimeError("JSONDatabase.base_path has not been set!")

        self.base_path.mkdir(parents=True, exist_ok=True)
        self.file_path = Path(self.base_path, filename)

        # Start off by reading the existing data from the file
        # (and if the file diesn't exist, initialise it with the provided initial data)
        try:
            self.load()
        except FileNotFoundError:
            self.data = self.get_initial_data(initial_data, initial_data_path)
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


def iso_to_locale_string(iso_date: str):
    """Parses an ISO-formatted date, and returns it formatted using the system locale"""
    parsed_date = date.fromisoformat(iso_date)
    locale_formatted_date = parsed_date.strftime("%x")
    return locale_formatted_date


def get_path_in_dictionary(dictionary: dict, *path):
    """Given a dictionary of nested dictionaries and values, gets the value at the specified path"""
    # Stores the dictionary we're checking (with the target somewhere inside), or the target item itself
    current_item = dictionary

    for key in path:
        try:
            current_item = current_item[key]
        except KeyError as error:
            # The specified path doesn't exist
            raise error

    # Finished searching, so we must have the requested value now
    return current_item
