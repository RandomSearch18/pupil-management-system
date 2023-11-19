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

    def add_input_widget(self, prompt: str):
        def submit():
            submit_button["state"] = DISABLED
            submitted_text.set(inputted_text.get())

        inputted_text = StringVar()
        submitted_text = StringVar()
        frame = Frame(self.parent)

        label = Label(frame, text=prompt.strip())
        label.grid(column=0, row=0)

        input_widget = Entry(frame, textvariable=inputted_text)
        input_widget.grid(column=1, row=0, padx=5)

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
