from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from app.interface.button import Button
from app.interface.label import Label
from app.session.session import session
from config.config import ICON_PATH


class Nav(QWidget):
    default_fullname = "Гость"
    default_btn_text = "Войти"

    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # logo
        logo = QLabel()
        pixmap = QPixmap(ICON_PATH)
        logo.setPixmap(pixmap)
        logo.setFixedSize(40, 40)
        logo.setScaledContents(True)
        self.main_layout.addWidget(logo)

        self.main_layout.addStretch()

        # fullname
        self.user_fullname = Label(self.default_fullname)
        self.main_layout.addWidget(self.user_fullname)
        self.main_layout.addSpacing(10)
        # auth button
        self.auth_btn = Button(self.default_btn_text)
        self.main_layout.addWidget(self.auth_btn)

    def update(self):
        if not session.user:
            self.user_fullname.setText(self.default_fullname)
            self.auth_btn.setText(self.default_btn_text)
        else:
            self.user_fullname.setText(session.user.get("fullname"))
            self.auth_btn.setText("Выйти")
