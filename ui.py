"""An abstract represnetation of a user interface, graphical or text-based"""


from app import App
from inputs import Inputs


class UI:
    def __init__(self, inputs: Inputs, app: App):
        self.inputs = inputs
        self.app = app
