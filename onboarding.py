"""Provides a guided introduction to the application, when it is first run."""
from __future__ import annotations
from typing import TYPE_CHECKING

from menu import Page, page_callback_wrapper

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
        print("""\
First, let's create an account. This identifies you as an individual, so you'll log in with it every time you use this program.

Create a new account for yourself by entering the required details at the prompts below.""")
        print()
        page_callback_wrapper(self.ui.create_account)

    def show(self):
        stages: dict[str, Page] = {
            "create_account": Page("Create account", self.create_account)
        }

        self.ui.breadcrumbs.push("Initial setup")

        if self.stage:
            stages[self.stage].execute(self.ui)
