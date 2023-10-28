"""Provides a guided introduction to the application, when it is first run."""
from __future__ import annotations
from typing import TYPE_CHECKING
from inputs import yes_no

from menu import Page, bold, clear_screen, page_callback_wrapper

if TYPE_CHECKING:
    from app import App
    from terminal_ui import TerminalUI


class Onboarding:
    def __init__(self, app: App, ui: TerminalUI) -> None:
        self.app = app
        self.ui = ui

        self.stage = self.app.settings_database.get("tui", "onboarding", "stage")

    def set_stage(self, stage: str):
        self.stage = stage
        self.app.settings_database.set("tui", "onboarding", "stage", value=stage)

    def create_account(self):
        self.set_stage("create_account")
        print()
        print(
            """\
First, let's create an account. This identifies you as an individual, so you'll log in with it every time you use this program.

Create a new account for yourself by entering the required details at the prompts below."""
        )
        print()
        page_callback_wrapper(self.ui.create_account)

    def ask_to_start_onboarding(self):
        clear_screen()
        print(f"Welcome to {bold(self.app.brand.APP_NAME)}!")
        print()
        print(
            """\
To help you get started with the program, you can be taken through a guided initial setup process.

Alternatively, you can go straight to the main menu and get set up on your own.""")
        print()

        should_start = yes_no("Start the guided initial setup? (yes/no) ")
        return should_start

    def show(self):
        stages: dict[str, Page] = {
            "create_account": Page("Create account", self.create_account)
        }

        self.ui.breadcrumbs.push("Initial setup")

        if not self.stage:
            should_continue = self.ask_to_start_onboarding()
            if not should_continue:
                # Prevent onboarding starting on future runs
                self.app.settings_database.set("tui", "onboarding", "show", value=False)
                return

            # Start with account creation
            self.set_stage("create_account")

        starting_stage = self.stage
        has_started = False
        for stage_id, stage_page in stages.items():
            if not has_started and not starting_stage == stage_id:
                # Skip this stage becuase it's before the starting_stage
                continue

            has_started = True
            stage_page.execute(self.ui)

        self.ui.breadcrumbs.pop()
