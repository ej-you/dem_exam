from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout

from app.interface.input import Input
from app.interface.label import Label


class FormInput(QVBoxLayout):
    def __init__(self, label_elem: Label, input_elem: Input, required: bool = False):
        super().__init__()

        self.addWidget(label_elem)
        self.addWidget(input_elem)
        self.setSpacing(10)

        # red asterisk
        if required:
            new_text = f"{label_elem.text()} <span style='color: red;'>*</span>"
            label_elem.setText(new_text)
            label_elem.setTextFormat(Qt.TextFormat.RichText) # for html


class FormInputList(QVBoxLayout):
    def __init__(self, elem_list: list[FormInput]):
        super().__init__()

        for elem in elem_list:
            self.addLayout(elem)
        self.setSpacing(25)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
