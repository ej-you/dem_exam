from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from app.interface.form import FormInputList, FormInput
from app.interface.input import InputText, InputPassword
from app.interface.label import Label
from app.interface.button import Button
from app.repo.db_session import DBSession
from app.repo.user import UserRepo, UserNotFoundError
from app.window.base import BaseWindow
from config.config import DEFAULT_WINDOW_TITLE
from app.session.session import session


class AuthWindow(BaseWindow):
    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Авторизация")

        self.user_repo = UserRepo(DBSession())

        username_lbl = Label("Логин")
        password_lbl = Label("Пароль")

        self.username = InputText("логин")
        self.password = InputPassword()

        input_list = FormInputList([
            FormInput(username_lbl, self.username),
            FormInput(password_lbl, self.password)
        ])
        input_list_container = QWidget()
        input_list_container.setFixedWidth(int(self.width() * 0.8))
        input_list_container.setLayout(input_list)

        submit_btn = Button("Войти")
        submit_btn.on_click(self._submit_btn_handler)
        guest_btn = Button("Войти как гость")
        guest_btn.on_click(self._quest_btn_handler)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(input_list_container)
        form_layout.addSpacing(30)
        form_layout.addWidget(submit_btn)
        form_layout.addWidget(guest_btn)

        main_widget = QWidget()
        main_widget.setLayout(form_layout)
        self.setCentralWidget(main_widget)

    def _open_good_list_window(self):
        self.app.show_good_list_window()
        self.close()

    def _submit_btn_handler(self):
        username = self.username.data
        password = self.password.data

        if not username or not password:
            self.status_bar.warn("Заполните все поля!")
            return

        try:
            user_data = self.user_repo.login(username, password)
            session.login(user_data)
        except UserNotFoundError as err:
            self.status_bar.warn(str(err))
            return
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Упс.. Неизвестная ошибка")
            return

        print("INFO: user login success")
        self._open_good_list_window()

    def _quest_btn_handler(self):
        print("INFO: login as guest")
        self._open_good_list_window()
