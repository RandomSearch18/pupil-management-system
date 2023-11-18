"""Mr Leeman's System: A pupil management system for Tree Road School
This project is for Task 3 of the lesson 2.2.1 Programming fundamentals - validation"""
import locale

from app import App
from terminal_ui import TerminalUI
from tkinter_ui import TkinterUI

# Use the current system locale for formatting dates/times
# See https://bugs.python.org/issue29457#msg287086
locale.setlocale(locale.LC_TIME, "")

# Initialise the application and the user interface
application = App()
terminal_ui = TerminalUI(application)

tkinter_ui = TkinterUI(application)
tkinter_ui.show()

# Execute the terminal UI
terminal_ui.show()
