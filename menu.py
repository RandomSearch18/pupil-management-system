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


class MenuItem:

    def __init__(self,
                 label: str,
                 should_show: Optional[Callable[[], bool]] = None):
        """A menu item is a single action that the user can select from a menu.
        label: The line of text that will be shown in the menu to represent the option
        should_show: An optional function that can return False to prevent the item from being included in the menu.
                     Useful for items that only make sense at certain times, e.g. to only show "Log out" if a user is logged in.
        """
        self.label = label
        self.should_show = should_show

    def execute(self):
        pass


class Option(MenuItem):

    def __init__(self,
                 label: str,
                 callback: Callable,
                 should_show: Optional[Callable[[], bool]] = None):
        """Create a menu item that can be added to menu.
        name: The text that is shown to the user, in the menu
        callback: The function to run when the user selects the option
        """
        super().__init__(label, should_show)
        self.callback = callback

    def execute(self):
        try:
            self.callback()
        except KeyboardInterrupt:
            print(color_wrap("\n" + "Aborted", COLOR_RED))


class Submenu(MenuItem):

    def execute(self):
        menu = Menu(self.options)
        menu.show()

    def __init__(self,
                 label: str,
                 title: str,
                 options: list[Option],
                 should_show: Optional[Callable[[], bool]] = None):
        super().__init__(label, should_show)
        self.should_show = should_show
        self.options = options
        self.title = title


class Menu:

    def show(self, loop=False):
        """Shows the menu to the user. It displays a list of possible actions and lets the user pick one of them.
        loop: Can be set to True to make the menu re-appear when the chosen action has completed.
              Useful for the main menu of the app, so multiple actions can be performed in one session.
        """

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

        # Execute the callback for the selected option
        selected_option = relevant_options[selection]
        selected_option.execute()

        if not loop:
            return

        print("\n")
        self.show(loop)

    def __init__(self, options: list[Option], title: Optional[str] = None):
        options = options or []
        self.options = options
        self.title = title
