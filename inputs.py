import hashlib
import re
from base64 import b64encode
from getpass import getpass

import bcrypt

## Text constants
icon_error = "❌"


def question(prompt) -> str:
    """Asks the user for input. Performs no input validation!"""
    # This is a seperate function in case we want to add styling to the prompts
    # in the future
    return input(f"{prompt}")


def text(prompt, error_message="Enter some text") -> str:
    """Asks the user for input, ensuring that they've entered at least 1 character"""
    raw_input = question(prompt)
    if not raw_input:
        print(f"{icon_error} {error_message}")
        return text(prompt)

    return raw_input


def username(prompt) -> str:
    """Usernames can be 1 to 64 characters. They must only be made up of word characters,
    periods, hyphens or spaces."""
    valid_username_regex = r"^[\w\.\- ]+$"

    raw_input = text(prompt, "Enter a username")
    length = len(raw_input)
    if not 1 <= length <= 64:
        print(f"{icon_error} Enter a username made up of 1–64 characters")
        return username(prompt)
    if not re.search(valid_username_regex, raw_input):
        print(f"{icon_error} Only use letters, numbers, ., -, _, and spaces")
        return username(prompt)

    return raw_input


def password_to_hash(raw_password: str) -> str:
    """Uses bcrypt to salt and hash the provided password, so that it can be stored safely.
    Returns the password hash encoded in Base64 as a string."""

    # To handle passwords that are over 72 characters long, we hash it using sha256 first
    # This is reccomended by https://pypi.org/project/bcrypt#maximum-password-length
    processed_password = b64encode(
        hashlib.sha256(raw_password.encode("utf-8")).digest())

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(processed_password, salt)
    return b64encode(hash).decode("utf-8")


def password(prompt, hide_characters=True):
    """A password must be at least 1 character, but has no other limitations.
    Returns a hashed and salted version of the password.
    By default, the typed text will be hidden from the user, but this can be disabled by setting hide_characters=False"""
    if not hide_characters:
        return password_to_hash(
            text(prompt, "Enter a password to keep your account secure"))

    raw_input = getpass(prompt)
    if not raw_input:
        print(f"{icon_error} Enter a password to keep your account secure")
        return password(prompt, hide_characters)

    return password_to_hash(prompt)
