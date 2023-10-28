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

    def create_account(self):
        print(self.ui.breadcrumbs.to_formatted())
        page_callback_wrapper(self.ui.create_account())

    def show(self):
        stages: dict[str, Page] = {
            "create_account": Page("Create acount", self.create_account)
        }

        self.ui.breadcrumbs.push("Initial setup")

        if self.stage:
            stages[self.stage].execute(self.ui)
