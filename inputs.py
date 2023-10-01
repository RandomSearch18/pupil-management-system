import hashlib
import unicodedata
from base64 import b64encode
from getpass import getpass

import bcrypt
import regex as re

from menu import error_incorrect_input
from util import process_password


def question(prompt) -> str:
    """Asks the user for input. Performs no input validation!"""
    # This is a seperate function in case we want to add styling to the prompts
    # in the future
    return input(f"{prompt}")


def text(prompt, error_message="Enter some text") -> str:
    """Asks the user for input that contains some text content.
    
    - Ensures that they've entered at least 1 non-whitespace character
    - Removes leading/trailing whitespace
    - Normalizes the unicode characters (composed and canonical form)
    """

    try:
        raw_input = question(prompt)
    except UnicodeDecodeError:
        # So, you thought it'd be funny to enter invalid UTF-8, eh?
        error_incorrect_input("Invalid character sequence")
        return text(prompt, error_message)

    # NFKC ensures that composed characters are used where possible, and also replaces
    # compatability characters with their canonical form, https://stackoverflow.com/a/16467505
    normalized_input = unicodedata.normalize("NFKC", raw_input.strip())

    if not normalized_input:
        error_incorrect_input(error_message)
        return text(prompt)

    return normalized_input


def new_username(prompt) -> str:
    """Usernames can be 1 to 64 characters. They must only be made up of word characters,
    periods, hyphens or spaces."""
    valid_username_regex = r"^[\w\.\- ]+$"

    raw_input = text(prompt, "Enter a username")
    length = len(raw_input)
    if not 1 <= length <= 64:
        error_incorrect_input("Enter a username made up of 1–64 characters")
        return new_username(prompt)
    if not re.search(valid_username_regex, raw_input):
        error_incorrect_input("Only use letters, numbers, ., -, _, and spaces")
        return new_username(prompt)

    return raw_input


def password_to_hash(raw_password: str) -> str:
    """Uses bcrypt to salt and hash the provided password, so that it can be stored safely.
    Returns the password hash encoded in Base64 as a string."""
    # Pre-process the password to work around bcrypt's 72-character limit
    processed_password = process_password(raw_password)

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(processed_password, salt)
    return b64encode(hash).decode("utf-8")


def password(prompt,
             error_message="Enter a password to authenticate",
             hide_characters=True):
    """Uses the getpass module to prevent the typed text being echoed,
    helping limit the effectiveness of sholder-surfing.
    This behaviour can be disabled by setting hide_characters=False."""
    if not hide_characters:
        return text(prompt, error_message)

    raw_input = getpass(prompt)
    if not raw_input:
        error_incorrect_input(error_message)
        return password(prompt, error_message, hide_characters)

    return raw_input


def new_password(prompt, hide_characters=True):
    """A password must be at least 1 character, but has no other limitations.
    Returns a hashed and salted version of the password.
    By default, the typed text will be hidden from the user, but this can be disabled by setting hide_characters=False"""
    error_message = "Enter a password to keep your account secure"

    if not hide_characters:
        return password_to_hash(
            password(prompt, error_message, hide_characters=False))

    return password_to_hash(password(prompt, error_message))


def name(prompt):
    """Names can include letters from any script, as well as spaces, hyphens and periods.
    Returns the name in title case.
    """
    # Allow any alphabetic character, any space charcater, hyphens and periods
    valid_name_regex = r"[\p{Alphabetic}\p{Z}\-\.']+"

    raw_input = text(prompt)
    if not re.match(valid_name_regex, raw_input):
        error_incorrect_input("Only use letters, ., -, ', and spaces")
        return name(prompt)

    return raw_input.title()
