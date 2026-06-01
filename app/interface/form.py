from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout

from app.interface.input import Input
from app.interface.label import Label


class FormInput(QVBoxLayout):
    def __init__(self, label_elem: Label, input_elem: Input):
        super().__init__()

        self.addWidget(label_elem)
        self.addWidget(input_elem)
        self.setSpacing(10)


class FormInputList(QVBoxLayout):
    def __init__(self, elem_list: list[FormInput]):
        super().__init__()

        for elem in elem_list:
            self.addLayout(elem)
        self.setSpacing(25)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
