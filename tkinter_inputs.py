from tkinter import DISABLED, StringVar, Tk, Widget
from tkinter.ttk import Button, Entry, Frame, Label
from inputs import Inputs


class TkinterInputs(Inputs):
    def __init__(self, window: Tk, target: Widget):
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
        input_row = InputRow(inputs=self)
        return input_row.get_response(prompt)

    def password(
        self,
        prompt,
        error_message="Enter a password to authenticate",
        hide_characters=True,
    ):
        return InputRow(self).get_response(prompt, hide_characters)


class InputRow:
    def __init__(self, inputs: TkinterInputs):
        self.inputs = inputs
        self.frame = None
        self.key_sequence_enter = "<Return>"
        self.just_submitted = False

    def draw(self, prompt, mask_characters=False):
        if self.frame:
            self.remove()

        self.inputted_text = StringVar()
        self.submitted_text = StringVar()
        self.frame = Frame(self.inputs.parent)

        label = Label(self.frame, text=prompt.strip())
        label.grid(column=0, row=0)

        mask_characters_with = "*" if mask_characters else ""
        self.input_entry = Entry(
            self.frame, textvariable=self.inputted_text, show=mask_characters_with
        )

        self.input_entry.grid(column=1, row=0, padx=5)
        self.input_entry.focus()

        self.submit_button = Button(self.frame, text="Next")
        self.submit_button.grid(column=3, row=0)

        self.frame_row = self.inputs.get_next_free_row()
        self.frame.grid(row=self.frame_row, column=0)
        self.inputs.displayed_inputs.append(self.frame)

    def remove(self):
        """Reverses InputRow#draw()"""
        self.frame.grid_remove()

    def activate(self):
        def submit(event=None):
            self.just_submitted = True
            self.submitted_text.set(self.inputted_text.get())
            self.deactivate()

        self.submit_button.config(command=submit)
        self.keybinding_enter = self.input_entry.bind(self.key_sequence_enter, submit)

    def get_response(self, prompt: str, mask_characters=False):
        self.draw(prompt, mask_characters)
        valid_response = False
        while not valid_response:
            self.activate()
            print("Waiting")
            # self.inputs.window.wait_variable(self.submitted_text)
            while True:
                if self.just_submitted:
                    break
                self.inputs.window.update_idletasks()
                self.inputs.window.update()
            print("Waiting done")
            valid_response = True

        return self.submitted_text.get()

    def deactivate(self):
        self.submit_button["state"] = DISABLED
        self.submit_button.unbind(self.key_sequence_enter, self.keybinding_enter)
