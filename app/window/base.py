from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from app.interface.status_bar import StatusBar
from config.config import DEFAULT_WINDOW_TITLE


class BaseWindow(QMainWindow):
    def __init__(self, app, title=DEFAULT_WINDOW_TITLE): # app: Application
        super().__init__()
        self.app = app

        self.setFixedSize(QSize(1500, 750))
        self.setWindowTitle(title)

        self.statusBar().showMessage("")
        self.status_bar = StatusBar(self.statusBar(), 3000)
