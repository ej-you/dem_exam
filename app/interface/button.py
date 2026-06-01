from typing import Callable

from PyQt6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, text):
        super().__init__()

        self.setText(text)

    def on_click(self, func: Callable):
        self.clicked.connect(func)
