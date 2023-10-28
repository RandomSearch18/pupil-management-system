import datetime
import unicodedata
from base64 import b64encode
from getpass import getpass

import bcrypt
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
import regex as re
from colorama import Style

from menu import color, error_incorrect_input
from util import process_password


def question(prompt) -> str:
    """Asks the user for input. Performs no input validation!"""
    # This is a seperate function in case we want to add styling to the prompts
    # in the future
    return input(f"{prompt}")


def valid_utf8(prompt):
    """Asks the user for input, returning a valid, normalised UTF-8 string"""
    try:
        raw_input = question(prompt)
    except UnicodeDecodeError:
        # So, you thought it'd be funny to enter invalid UTF-8, eh?
        error_incorrect_input("Invalid character sequence")
        return valid_utf8(prompt)

    # NFKC ensures that composed characters are used where possible, and also replaces
    # compatability characters with their canonical form, https://stackoverflow.com/a/16467505
    return unicodedata.normalize("NFKC", raw_input.strip())


def text(prompt, error_message="Enter some text") -> str:
    """Asks the user for input that contains some text content.

    - Ensures that they've entered at least 1 non-whitespace character
    - Removes leading/trailing whitespace
    - Normalizes the unicode characters (composed and canonical form)
    """
    stripped_input = valid_utf8(prompt).strip()

    if not stripped_input:
        error_incorrect_input(error_message)
        return text(prompt)

    return stripped_input


def multiline(prompt, error_message: str = "Enter some text"):
    """Asks the user to input text, allowing line breaks

    - This essentially fakes a multiline input by calling input() in a loop
    - It validates that some text was entered
    - Pressing enter on an empty line submits the input
    """
    print(
        prompt
        + color("(Enter to insert newlines; press Enter twice to submit)", Style.DIM)
    )

    lines = []
    while True:
        line = valid_utf8("")
        if line == "":
            break
        # Preserve indentation but remove trailing spaces
        line.rstrip()
        lines.append(line)

    full_input = "\n".join(lines)

    # Validate that they actually entered something
    if full_input.strip() == "":
        error_incorrect_input(error_message)
        return multiline(prompt, error_message)

    return full_input


def integer(prompt, error_message: str = "Enter a valid whole number") -> int:
    """Asks for a valid integer to be input"""
    raw_input = text(prompt, "Enter at least 1 digit")
    try:
        int_input = int(raw_input)
    except ValueError:
        error_incorrect_input(error_message)
        return integer(prompt, error_message)

    return int_input


def yes_no(prompt, error_message = 'Enter "yes" or "no"') -> bool:
    """Asks for a boolean (yes or no) response"""
    YES_ANSWERS = ["yes", "y", "t", "true", "1", ":thumbs_up:"]
    NO_ANSWERS = ["no", "n", "f", "false", "0", ":thumbs_down:"]
    
    lowercase_input = text(prompt, error_message).lower()
    if lowercase_input in YES_ANSWERS:
        return True
    if lowercase_input in NO_ANSWERS:
        return False
    
    return yes_no(prompt, error_message)


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


def password(
    prompt, error_message="Enter a password to authenticate", hide_characters=True
):
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
    By default, the typed text will be hidden from the user, but this can be disabled by setting hide_characters=False
    """
    error_message = "Enter a password to keep your account secure"

    if not hide_characters:
        return password_to_hash(password(prompt, error_message, hide_characters=False))

    return password_to_hash(password(prompt, error_message))


def name(prompt):
    """Names can include letters from any script, as well as spaces, hyphens and periods.
    Returns the name in title case."""
    # Allow any alphabetic character, any space charcater, hyphens and periods
    valid_name_regex = r"^[\p{Alphabetic}\p{Z}\-\.']+$"

    raw_input = text(prompt)
    if not re.match(valid_name_regex, raw_input):
        error_incorrect_input("Only use letters, ., -, ', and spaces")
        return name(prompt)

    return raw_input.title()


def date(prompt) -> datetime.date:
    """Prompts the user to input a date in YYYY-MM-DD format."""
    # Rule 1 of dealing with timezones: Don't deal with timezones
    raw_input = text(prompt)

    try:
        parsed_date = datetime.date.fromisoformat(raw_input)
    except ValueError:
        error_incorrect_input("Enter a valid date in the format YYYY-MM-DD")
        return date(prompt)

    if parsed_date > datetime.date.today():
        error_incorrect_input("Enter a date that's in the past")
        return date(prompt)

    return parsed_date


def tutor_group(prompt):
    """Prompts the user to input a tutor group

    - Normalises the returned tutor group to be in uppercase
    - Checks that the input's in the format of a tutor group
    - Doesn't check that the input is a sutor group that actually exists
    Note: The spec doesn't really explain how tutor groups are meant to work"""
    # Allow 1+ digits followed by 1+ capital letters, e.g 7CA or 12A
    tutor_group_regex = r"^(\d+)([A-Z]+)$"

    raw_input = text(prompt).upper()

    if not re.match(tutor_group_regex, raw_input):
        error_incorrect_input("Enter a tutor group in a format like 13AX")
        return tutor_group(prompt)

    return raw_input


def phone_number(prompt):
    """Prompts the user to input a valid UK or international phone number"""
    raw_input = text(prompt)

    try:
        parsed_phone_number = phonenumbers.parse(raw_input, "GB")
    except NumberParseException:
        error_incorrect_input("Enter a phone number (UK or international format)")
        return phone_number(prompt)

    if not phonenumbers.is_possible_number(parsed_phone_number):
        error_incorrect_input("Enter a correctly-formatted phone number")
        return phone_number(prompt)

    serialized_phone_number = phonenumbers.format_number(
        parsed_phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )
    return serialized_phone_number
