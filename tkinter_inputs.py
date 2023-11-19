from tkinter import DISABLED, StringVar, Tk, Widget
from tkinter.ttk import Button, Entry, Frame, Label
from inputs import Inputs


class TkinterInputs(Inputs):
    def __init__(self, window: Tk, target: Widget) -> None:
        super().__init__()
        self.window = window
        self.parent = target
        self.displayed_inputs = []

    def get_next_free_row(self):
        return len(self.displayed_inputs)

    def add_input_widget(self, prompt: str, mask_characters=False):
        def submit(event=None):
            submit_button["state"] = DISABLED
            submit_button.unbind(key_sequence, enter_keybinding)
            submitted_text.set(inputted_text.get())

        inputted_text = StringVar()
        submitted_text = StringVar()
        frame = Frame(self.parent)

        label = Label(frame, text=prompt.strip())
        label.grid(column=0, row=0)

        mask_characters_with = "*" if mask_characters else ""
        input_widget = Entry(
            frame, textvariable=inputted_text, show=mask_characters_with
        )
        key_sequence = "<Return>"
        enter_keybinding = input_widget.bind(key_sequence, submit)
        input_widget.grid(column=1, row=0, padx=5)
        input_widget.focus()

        submit_button = Button(frame, text="Next", command=submit)
        submit_button.grid(column=3, row=0)

        frame_row = self.get_next_free_row()
        frame.grid(row=frame_row, column=0)
        self.displayed_inputs.append(frame)

        return submitted_text

    def question(self, prompt) -> str:
        submitted_text = self.add_input_widget(prompt)
        # self.window.mainloop()
        self.window.wait_variable(submitted_text)
        return submitted_text.get()

    def password(
        self,
        prompt,
        error_message="Enter a password to authenticate",
        hide_characters=True,
    ):
        submitted_text = self.add_input_widget(prompt, hide_characters)
        self.window.wait_variable(submitted_text)
        return submitted_text.get()
