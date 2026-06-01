from PyQt6.QtWidgets import QWidget

from app.interface.button import Button
from app.interface.nav import Nav
from app.session.session import session
from app.window.base import BaseWindow
from config.config import DEFAULT_WINDOW_TITLE


class GoodListWindow(BaseWindow):
    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Список товаров")

        # navbar
        self.nav = Nav()
        self.nav.auth_btn.on_click(self._auth_btn_handler)
        self.setMenuWidget(self.nav)

        # content
        self.btn = Button("Press me")
        self.setCentralWidget(self.btn)

    def _open_auth_window(self):
        self.app.show_auth_window()
        self.close()

    def _auth_btn_handler(self):
        session.logout()
        print("INFO: logout")
        self._open_auth_window()
