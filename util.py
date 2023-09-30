import json
from pathlib import Path
from typing import Any


class JSONDatabase():
    # By default, store data in the current directory
    base_path = Path(".")

    def save(self):
        """Saves the database to disk, ensuring that the file contents matches the in-memory contents."""
        with open(self.file_path, "w") as file:
            json.dump(self.data, file)

    def load(self):
        """Loads the contents of the database file into memory, so that the data can be accessed."""
        with open(self.file_path, "r") as file:
            self.data = json.load(file)

    def __init__(self, filename: str, initial_data: Any):
        self.file_path = Path(self.base_path, filename)

        # Start off by reading the existing data from the file
        # (and if the file diesn't exist, initialise it with the provided initial data)
        try:
            self.load()
        except FileNotFoundError:
            with open(self.file_path, "w") as new_file:
                json.dump(initial_data, new_file)


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
