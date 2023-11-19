from curses import window
from tkinter import Tk, ttk

from app import App
from tkinter_inputs import TkinterInputs
from ui import UI


class TkinterUI(UI):
    """An experimental graphical user interface to the app"""

    def __init__(self, app: App) -> None:
        self.window = Tk()
        self.inputs_frame = ttk.Frame(padding=5)
        self.inputs_frame.grid(column=0, row=0)
        inputs = TkinterInputs(self.window, self.inputs_frame)
        super().__init__(inputs, app)

    def on_window_close(self):
        self.window.destroy()
        # exit()

    def show(self):
        # self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)

        # Use the Clam theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.log_in()
        self.window.after(100, self.window.destroy)
        self.window.mainloop()
        # self.window.destroy()
        # self.window.mainloop()
        print("Finished Tkinter UI")
