import os
import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from app.window.auth import AuthWindow
from app.window.good import GoodWindow
from app.window.good_list import GoodListWindow
from config.config import MEDIA_PREFIX


class Application:
    def __init__(self):
        self.__app = QApplication(sys.argv)

        font = QFont("Times New Roman", 14)
        self.__app.setFont(font)

        self.auth_window = AuthWindow(self)
        self.good_list_window = GoodListWindow(self)
        self.good_window = GoodWindow(self)

    def start(self):
        os.makedirs(MEDIA_PREFIX, exist_ok=True)
        sys.exit(self.__app.exec())

    def show_auth_window(self):
        self.auth_window.show()

    def show_good_list_window(self):
        self.good_list_window.show()

    def show_good_window(self, pk: int, new: bool):
        self.good_window.show(pk, new)
