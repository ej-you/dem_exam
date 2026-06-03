from PyQt6.QtWidgets import QWidget, QHBoxLayout

from app.interface.scroll_list import ScrollList
from app.repo.db_session import DBSession
from app.repo.good import GoodRepo
from app.window.base import BaseWindowWithNavbar
from config.config import DEFAULT_WINDOW_TITLE


class GoodListWindow(BaseWindowWithNavbar):
    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Список товаров")

        self.good_repo = GoodRepo(DBSession())

        # content
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

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
        # TODO: button to add a new good
        main_layout.addLayout(scroll_list)

    def _open_good_window(self, pk: int):
        self.app.show_good_window(pk)
        self.close()
        print(f"INFO: open {pk} good")
