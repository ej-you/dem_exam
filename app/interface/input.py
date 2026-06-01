from PyQt6.QtWidgets import QLineEdit, QDoubleSpinBox, QSpinBox, QWidget


class Input(QWidget):
    def __init__(self):
        super().__init__()

    @property
    def data(self):
        return


class InputInteger(QSpinBox, Input):
    def __init__(self, value: int = 0, minimum: int = 0, maximum: int = 100):
        super().__init__()

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)

    @property
    def data(self):
        return self.value()


class InputNumber(QDoubleSpinBox, Input):
    def __init__(self, value: float = 0, minimum: float = float("-inf"), maximum: float = float("inf")):
        super().__init__()

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)

    @property
    def data(self):
        return self.value()


class InputText(QLineEdit, Input):
    def __init__(self, placeholder: str = "введите текст...", text: str = ""):
        super().__init__()

        self.setPlaceholderText(placeholder)
        self.setText(text)

    @property
    def data(self):
        return self.text()


class InputPassword(InputText):
    def __init__(self):
        super().__init__("пароль")

        self.setEchoMode(self.EchoMode.Password)
