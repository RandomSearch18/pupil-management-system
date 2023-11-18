from tkinter import Tk, ttk

from app import App
from tkinter_inputs import TkinterInputs
from ui import UI


class TkinterUI(UI):
    """An experimental graphical user interface to the app"""

    def __init__(self, app: App) -> None:
        inputs = TkinterInputs()
        super().__init__(inputs, app)

    def show(self):
        self.window = Tk()

        # Use the Clam theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.window.mainloop()
