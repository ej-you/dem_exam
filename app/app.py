import sys

from PyQt6.QtWidgets import QApplication

from app.window.auth import AuthWindow
from app.window.good import GoodWindow
from app.window.good_list import GoodListWindow


class Application:
    def __init__(self):
        self.__app = QApplication(sys.argv)

        self.auth_window = AuthWindow(self)
        self.good_list_window = GoodListWindow(self)
        self.good_window = GoodWindow(self)

    def start(self):
        sys.exit(self.__app.exec())

    def show_auth_window(self):
        self.auth_window.show()

    def show_good_list_window(self):
        self.good_list_window.show()

    def show_good_window(self, pk: int):
        self.good_window.show(pk)
