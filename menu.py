"""A menu-driven interface based around the Menu and Option classes"""
from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Literal, Optional

from colorama import Fore, Style

if TYPE_CHECKING:
    from terminal_ui import Breadcrumbs, TerminalUI


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


def clear_screen():
    """Clears the screen/terminal (preserving scrollback)"""
    # https://stackoverflow.com/a/50560686
    print("\033[H\033[J", end="")


def wait_for_enter_key(text = "Press Enter to continue..."):
    """Pauses the terminal, i.e. waits for the user to press Enter before continuing"""
    return input(color(text, Style.DIM))


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
        raw_input = input("Pick an option: ")
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

    def execute(self, ui: TerminalUI):
        pass


def page_callback_wrapper(callback):
    """Runs the callback for a page until it returns a success code or raises an error"""
    result = 1
    while isinstance(result, int) and result > 0:
        # The callback returned a positive number, so it wants to be restarted
        result = callback()


class Page(MenuItem):
    """Pages are sections of the UI for viewing inforomation or perfoming an action"""

    def __init__(self,
                 label: str,
                 callback: Callable,
                 should_show: Optional[Callable[[], bool]] = None,
                 description: Optional[str] = None,
                 title: Optional[str] = None,
                 clear_at_start = True,
                 pause_at_end = True):
        super().__init__(label, should_show, description)
        self.title = title or label or callback.__name__
        self.callback = callback
        self.clear_at_start = clear_at_start
        self.pause_at_end = pause_at_end
        self.breadcrumbs = None

    def execute(self, ui: TerminalUI, error_handling: Literal["restart", "return"] = "restart"):
        try:
            if self.clear_at_start:
                clear_screen()

            self.before_foreward_navigation(ui)

            # Actually run the page
            page_callback_wrapper(self.callback)

            if self.pause_at_end:
                print()
                wait_for_enter_key()

            self.before_backward_navigation(ui)
        except KeyboardInterrupt as error:
            print(color("\n" + "Aborted", Fore.RED))
            self.before_backward_navigation(ui)
            raise error
            
        except Exception as error:
            error_type = type(error).__name__
            error_text = f"{error_type}: {error}"

            print(color(f"Encountered an error while running '{self.title}'", Fore.RED))
            print(color(error_text, Fore.RESET))

            print()
            action_part = "return to the previous screen" if error_handling == "return" else "try again"
            inputted_text = wait_for_enter_key(f"Press Enter to {action_part}...")

            # Hidden feature: Type "RAISE" at the prompt to re-raise the exception
            if inputted_text.lower() == "raise":
                raise error

            # Restart the page or go back to the previous page according to error_handling parameter
            if error_handling == "restart":
                # TODO: Bail out and go back to previous page if there have been too many errors
                # Future idea: Give the user a menu to chose what to do, e.g. go back, restart page, debug error
                self.before_backward_navigation(ui)
                return self.execute(ui, error_handling)
            if error_handling == "return":
                self.before_backward_navigation(ui)
                return


    def before_foreward_navigation(self, ui: TerminalUI):
        """Called just before the user "enters into" the page"""
        ui.breadcrumbs.push(self.title)
        title_line = ui.breadcrumbs.to_formatted()
        print(title_line)
    
    def before_backward_navigation(self, ui: TerminalUI):
        """Called just before the user "exits out of" the page, i.e. after the callback has reutned"""
        ui.breadcrumbs.pop()

class Submenu(MenuItem):

    def execute(self, ui):
        # FIXME update breadcrumbs here (probably)
        menu = Menu(self.options, ui)
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


    def show(self, loop=False, error_handling: Literal["restart", "return"] = "restart"):
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
        clear_screen()

        # If any of the items have descriptions, we add more padding (line breaks) to the menu
        # to keep it readable and to seperate out the options.
        use_extra_linebreaks = self.uses_descriptions()

        print(self.ui.breadcrumbs.to_formatted())
        if use_extra_linebreaks:
            # Padding between the breadcrumbs and the options
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
        try:
            selected_option.execute(ui=self.ui, error_handling=error_handling)
        except KeyboardInterrupt:
            # If the user cancels the page, treat it as if the page exited cleanly
            pass

        if not loop:
            return

        self.show(loop)

    def __init__(self, options: list[MenuItem], ui: TerminalUI):
        self.options = options or []
        self.ui = ui
