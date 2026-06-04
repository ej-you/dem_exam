from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from app.interface.nav import Nav
from app.interface.status_bar import StatusBar
from app.session.session import session
from config.config import DEFAULT_WINDOW_TITLE


class BaseWindow(QMainWindow):
    def __init__(self, app, title=DEFAULT_WINDOW_TITLE): # app: Application
        super().__init__()
        self.app = app

        self.setFixedSize(QSize(1500, 800))
        self.setWindowTitle(title)

        self.statusBar().showMessage("")
        self.status_bar = StatusBar(self.statusBar(), 3000)

class BaseWindowWithNavbar(BaseWindow):
    def __init__(self, app, title=DEFAULT_WINDOW_TITLE): # app: Application
        super().__init__(app, title)

        # navbar
        self.nav = Nav()
        self.nav.auth_btn.on_click(self._auth_btn_handler)
        self.setMenuWidget(self.nav)

    def _auth_btn_handler(self):
        session.logout()
        print("INFO: logout")
        self.app.show_auth_window()
        self.close()

    def show(self):
        self.nav.update()
        super().show()
