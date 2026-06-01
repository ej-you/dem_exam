from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QStatusBar


class StatusBar:
    def __init__(self, inst: QStatusBar, delay: int):
        self.inst = inst
        self.delay = delay

    @staticmethod
    def _style_with_color(hex_color: str) -> str:
        return f"""
            QStatusBar {{
                background-color: {hex_color};
                color: white;
                font-weight: bold;
            }}
        """

    def _show_message(self, hex_color: str, text: str):
        self.inst.setStyleSheet(self._style_with_color(hex_color))
        self.inst.showMessage(text, self.delay)
        QTimer.singleShot(self.delay, lambda: self.inst.setStyleSheet(""))

    def info(self, text: str):
        self._show_message("#21bc36", "ИНФО: "+text)

    def warn(self, text: str):
        self._show_message("#8c7b1b", "ВНИМАНИЕ: "+text)

    def error(self, text: str):
        self._show_message("#ff4444", "ОШИБКА: "+text)
