from PyQt6.QtWidgets import QWidget, QVBoxLayout

from app.entity.user import Role
from app.interface.button import Button
from app.interface.scroll_list import ScrollList
from app.repo.db_session import DBSession
from app.repo.good import GoodRepo
from app.session.session import session
from app.window.base import BaseWindowWithNavbar
from config.config import DEFAULT_WINDOW_TITLE


class GoodListWindow(BaseWindowWithNavbar):
    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Список товаров")

        self.good_repo = GoodRepo(DBSession())

        # content
        # self.main_widget = QWidget()
        # self.setCentralWidget(self.main_widget)
        # self.main_layout = QVBoxLayout(self.main_widget)

        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)

        self.content_widget = QWidget()
        self.container_layout.addWidget(self.content_widget)

        self._update_content()

    def _update_content(self):
        old_widget = self.content_widget
        self.content_widget = QWidget()

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

        layout = QVBoxLayout(self.content_widget)

        # TODO: add filters, sorting, search
        if session.user and session.user.get("role") == Role.admin:
            new_good_btn = Button("Новый товар")
            new_good_btn.on_click(lambda: self._open_good_window(0, new=True))
            layout.addWidget(new_good_btn)

        layout.addLayout(scroll_list)
        self.container_layout.replaceWidget(old_widget, self.content_widget)
        old_widget.deleteLater()

    def _open_good_window(self, pk: int, new: bool = False):
        self.app.show_good_window(pk, new)
        self.close()
        print(f"INFO: open {pk} good")

    def show(self):
        self._update_content()
        super().show()
