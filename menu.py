"""A menu-driven interface based around the Menu and Option classes"""
from typing import Callable, Optional

from colorama import Fore, Style


def error_incorrect_input(message: str):
    """Prints a error message to notify the user that their inputed text is incorrect.
    They should immediately be given the option to retry."""
    print(color(f"❌ {message}", Fore.RED))


def print_hint(hint: str):
    """Hints are deemphasized lines of text that go above an input,
    providing tips, hints, context or description relavant to that input."""
    print(color(hint, Style.DIM))


def info_line(field: str, data):
    """Prints a piece of data with a label (on a single line)
    
    - The field is the label for the data
    - The data parameter is the actual data, e.g. a number or a string
    - Formats the content to be bold
    """
    label_part = f"{field.strip()}: "
    content_part = bold(str(data))
    print(label_part + content_part)


def clear():
    """Clears the screen/terminal (preserving scrollback)"""
    # https://stackoverflow.com/a/50560686
    print("\033[H\033[J", end="")


def bold(string: str) -> str:
    """Makes the provided string bold, using ANSI escape codes"""
    return color(string, Style.BRIGHT)


def color(string: str, color: str) -> str:
    """Applies an ANSI colour code to a string"""
    return f"{color}{string}{Style.RESET_ALL}"


def get_selection(max: int) -> Optional[int]:
    """Asks the user to pick a 1-indexed number up to (and including) `max`,
    returing it as zero-indexed."""
    try:
        raw_input = input("Make a selection: ")
    except KeyboardInterrupt:
        print(color("Cancelled!", Fore.RED))
        return None

    if not raw_input.isnumeric():
        error_incorrect_input("Your selection must be a positive number!")
        return get_selection(max)

    selection = int(raw_input)
    if selection < 0:
        error_incorrect_input("Select a positive number!")
        return get_selection(max)
    if selection > max:
        error_incorrect_input(
            f"Selection out of bounds: Must be below {max+1}")
        return get_selection(max)

    # If they entered 0, we assume that they want to exit the selection
    if selection == 0:
        return None

    # Subtract one from the selection, since the user is given options that are
    # indexed from 1, but we want them to be zero-indexed
    selection -= 1
    return selection


class MenuItem:

    def __init__(self,
                 label: str,
                 should_show: Optional[Callable[[], bool]] = None,
                 description: Optional[str] = None):
        """A menu item is a single action that the user can select from a menu.
        label: The line of text that will be shown in the menu to represent the option
        should_show: An optional function that can return False to prevent the item from being included in the menu.
                     Useful for items that only make sense at certain times, e.g. to only show "Log out" if a user is logged in.
        description: An optional piece of text that will be shown (desaturated) above the option to provide additional context.
        """
        self.label = label
        self.should_show = should_show
        self.description = description

    def execute(self):
        pass


class Option(MenuItem):

    def __init__(self,
                 label: str,
                 callback: Callable,
                 should_show: Optional[Callable[[], bool]] = None,
                 description: Optional[str] = None):
        """Create a menu item that can be added to menu.
        name: The text that is shown to the user, in the menu
        callback: The function to run when the user selects the option
        """
        super().__init__(label, should_show, description)
        self.callback = callback

    def execute(self):
        try:
            self.callback()
        except KeyboardInterrupt:
            print(color("\n" + "Aborted", Fore.RED))


class Submenu(MenuItem):

    def execute(self):
        menu = Menu(self.options, self.title)
        menu.show()

    def __init__(self,
                 label: str,
                 title: str,
                 options: list[MenuItem],
                 should_show: Optional[Callable[[], bool]] = None):
        super().__init__(label, should_show)
        self.should_show = should_show
        self.options = options
        self.title = title


class Menu:
    def uses_descriptions(self) -> bool:
        """Returns True if any of the menu items have descriptions"""
        for item in self.options:
            if item.description:
                return True
        return False


    def show(self, loop=False):
        """Shows the menu to the user. It displays a list of possible actions and lets the user pick one of them.
        loop: Can be set to True to make the menu re-appear when the chosen action has completed.
              Useful for the main menu of the app, so multiple actions can be performed in one session.
        """

        # Go through all the options and add the ones that should be shown
        relevant_options: list[MenuItem] = []
        for option in self.options:
            if option.should_show is not None:
                if option.should_show():
                    relevant_options.append(option)
            else:
                relevant_options.append(option)

        # Handle the case of no available options
        if len(relevant_options) == 0:
            print(color("No options available. Goodbye!", Fore.RED))
            return
        
        print("AAA")
        clear()

        # If any of the items have descriptions, we add more padding (line breaks) to the menu
        # to keep it readable and to seperate out the options.
        use_extra_linebreaks = self.uses_descriptions()

        if self.title:
            print(bold(self.title))
            if use_extra_linebreaks:
                # Padding between title and options
                print()

        # Print each option on its own line
        for i, option in enumerate(relevant_options):
            if use_extra_linebreaks and i > 0:
                # Padding betweem each option
                print()

            if option.description:
                print_hint(option.description)

            print(f"{i+1}) {option.label}")

        if use_extra_linebreaks:
            # Padding between options and selection input
            print()

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

        self.show(loop)

    def __init__(self, options: list[MenuItem], title: Optional[str] = None):
        options = options or []
        self.options = options
        self.title = title
