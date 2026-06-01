from PyQt6.QtWidgets import QWidget, QHBoxLayout

from app.interface.button import Button
from app.interface.nav import Nav
from app.interface.scroll_list import ScrollList
from app.repo.db_session import DBSession
from app.repo.good import GoodRepo
from app.session.session import session
from app.window.base import BaseWindow
from config.config import DEFAULT_WINDOW_TITLE


class GoodListWindow(BaseWindow):
    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Список товаров")

        self.good_repo = GoodRepo(DBSession())

        # navbar
        self.nav = Nav()
        self.nav.auth_btn.on_click(self._auth_btn_handler)
        self.setMenuWidget(self.nav)

        # content
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        main_layout = QHBoxLayout()
        self.main_widget.setLayout(main_layout)

        try:
            good_list = self.good_repo.get_all()
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Упс.. Неизвестная ошибка")
            return
        scroll_list = ScrollList(
            header_labels=["Артикул", "Название", "Цена"],
            data_keys=["article", "title", "price"],
            data=good_list,
            on_click_handler=self._open_good_window
        )

        # TODO: add filters, sorting, search
        main_layout.addLayout(scroll_list)

    def _open_good_window(self, pk: int):
        # self.app.show_good_window(pk) TODO
        # self.close()
        print(f"open {pk} good")

        # def open_good_card(self, good_id: int):
        #     """Открывает карточку товара"""
        #     from app.window.good_card import GoodCardWindow
        #     self.good_card_window = GoodCardWindow(self.app, good_id)
        #     self.good_card_window.show()
        #     self.close()

    def _open_auth_window(self):
        self.app.show_auth_window()
        self.close()

    def _auth_btn_handler(self):
        session.logout()
        print("INFO: logout")
        self._open_auth_window()
