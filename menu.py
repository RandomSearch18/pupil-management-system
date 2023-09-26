"""A menu-driven interface based around the Menu and Option classes"""
from typing import Callable, Optional

# Terminal colour codes
COLOR_RED = "\x1b[31m"


def color_wrap(string: str, color: str) -> str:
    """Applies an ANSI colour code to a string"""
    return f"{color}{string}\033[0m"


def get_selection(max: int) -> int | None:
    """Asks the user to pick a 1-indexed number up to (and including) `max`,
    returing it as zero-indexed."""
    try:
        raw_input = input("Make a selection: ")
    except KeyboardInterrupt:
        print(color_wrap("Selection cancelled!", COLOR_RED))
        return None

    if not raw_input.isnumeric():
        print("Your selection must be a positive number!")
        return get_selection(max)

    selection = int(raw_input)
    if selection < 0:
        print("Select a positive number!")
        return get_selection(max)
    if selection > max:
        print("Selection out of bounds: Must be below", max)
        return get_selection(max)

    # Subtract one from the selection, since the user is given options that are
    # indexed from 1, but we want them to be zero-indexed
    selection -= 1
    return selection


class Option:

    def __init__(self,
                 label: str,
                 callback: Callable,
                 should_show: Optional[Callable[[], bool]] = None):
        """Create a menu item that can be added to menu.
        name: The text that is shown to the user, in the menu
        callback: The function to run when the user selects the option
        should_show: An optional function that can return False to prevent the option from being shown
        """
        self.label = label
        self.callback = callback
        self.should_show = should_show


class Menu:

    def show(self, loop=False):
        """Shows the menu to the user. It displays a list of options and lets the user
        pick one of them."""

        # Go through all the options and add the ones that should be shown
        relevant_options: list[Option] = []
        for option in self.options:
            if option.should_show is not None:
                if option.should_show():
                    relevant_options.append(option)
            else:
                relevant_options.append(option)

        # Handle the case of no available options
        if len(relevant_options) == 0:
            print("No options available. Goodbye!")
            return

        if self.title:
            print(self.title)

        # Print each option on its own line
        for i, option in enumerate(relevant_options):
            print(f"{i+1}) {option.label}")

        # Ask the user to select a option number
        selection = get_selection(len(relevant_options))

        if selection is None:
            # Exit the menu if the user entered "0" (to cancel the selection)
            return

        print()
        callback = relevant_options[selection].callback

        try:
            # Actually run the callback
            callback()
        except KeyboardInterrupt:
            print(color_wrap("\n" + "Aborted", COLOR_RED))

        if not loop:
            return

        print("\n")
        self.show(loop)

    def __init__(self, options: list[Option], title: Optional[str] = None):
        options = options or []
        self.options = options
        self.title = title
