from tkinter import IntVar, StringVar, Tk, Widget
from tkinter.ttk import Entry, Frame, Label
from inputs import Inputs


class TkinterInputs(Inputs):
    def __init__(self, window: Tk, target: Widget) -> None:
        super().__init__()
        self.window = window
        self.parent = target
        self.displayed_inputs = []

    def get_next_free_row(self):
        return len(self.displayed_inputs)

    def add_input_widget(self, prompt: str, input_widget: Widget):
        frame = Frame(self.parent)

        label = Label(frame, text=prompt.strip())
        label.grid(column=0, row=0)

        input_widget.master = frame
        input_widget.grid(column=1, row=0)

        frame_row = self.get_next_free_row()
        frame.grid(row=frame_row)
        self.displayed_inputs.append(frame)

    def question(self, prompt) -> str:
        text = StringVar()
        input_widget = Entry(textvariable=text)
        self.add_input_widget(prompt, input_widget)
        # self.window.mainloop()
        self.window.wait_variable(text)
