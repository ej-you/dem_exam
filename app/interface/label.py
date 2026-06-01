from PyQt6.QtWidgets import QLabel


class Label(QLabel):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
