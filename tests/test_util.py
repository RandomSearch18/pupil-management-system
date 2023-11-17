from contextlib import contextmanager
from locale import LC_TIME, getlocale, setlocale
import util


@contextmanager
def use_locale(category: int, locale_string: str):
    # Taken from https://stackoverflow.com/a/50737946
    prev_locale_string = getlocale(category)
    setlocale(category, locale_string)
    yield
    setlocale(category, prev_locale_string)


def test_iso_to_locale_string():
    iso_date_string = "1984-11-30"

    with use_locale(LC_TIME, "en_US.utf8"):
        # Check that it can correctly use the worst date format
        formatted_date = util.iso_to_locale_string(iso_date_string)
        assert formatted_date == "11/30/1984"
