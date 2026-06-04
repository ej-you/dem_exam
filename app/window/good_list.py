from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from app.entity.user import Role
from app.interface.button import Button
from app.interface.input import InputText, ComboBox
from app.interface.label import Label
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

        self.filter = 0
        self.search = ""
        self.sort = ""

        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)

        # Кнопка нового товара
        self.new_good_btn = Button("Новый товар")
        self.new_good_btn.on_click(lambda: self._open_good_window(0, new=True))
        self.new_good_btn.setVisible(True if session.user and session.user.get("role") == Role.admin else False)
        self.container_layout.addWidget(self.new_good_btn)

        # Панель фильтров
        self.filters_widget = self._create_filters()
        show_filters = session.user and ((role := session.user.get("role")) == Role.admin or role == Role.manager)
        self.filters_widget.setVisible(True if show_filters else False)
        self.container_layout.addWidget(self.filters_widget)

        self.content_widget = QWidget()
        self.container_layout.addWidget(self.content_widget)
        self.content_layout = QVBoxLayout(self.content_widget)

        # scroll list container
        self.data_container = QWidget()
        self.data_layout = QVBoxLayout(self.data_container)
        self.content_layout.addWidget(self.data_container)
        # load data
        self._update_content()

    def _update_content(self):
        # update new good btn visible
        self.new_good_btn.setVisible(True if session.user and session.user.get("role") == Role.admin else False)
        # update filters visible
        show_filters = session.user and ((role := session.user.get("role")) == Role.admin or role == Role.manager)
        self.filters_widget.setVisible(True if show_filters else False)
        # update scroll list
        self._update_scroll_list()

    def _update_scroll_list(self):
        # clean data_layout (not recreate data_container)
        while self.data_layout.count():
            item = self.data_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    subitem = item.layout().takeAt(0)
                    if subitem.widget():
                        subitem.widget().deleteLater()

        try:
            good_list = self.good_repo.get_all(self.filter, self.search, self.sort)
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

        self.data_layout.addLayout(scroll_list)

    def _create_filters(self):
        filter_panel = QWidget()
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setSpacing(15)

        filter_layout.addWidget(Label("Поиск:"))
        self.search_input = InputText(placeholder="Артикул, название, описание...")
        self.search_input.textChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.search_input)

        filter_layout.addWidget(Label("Поставщик:"))
        self.supplier_filter = ComboBox()
        self.supplier_filter.addItem("Все", 0)
        for supplier in self.good_repo.get_all_suppliers():
            self.supplier_filter.addItem(supplier.get("title"), supplier.get("id"))
        self.supplier_filter.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.supplier_filter)

        filter_layout.addWidget(Label("Сортировка:"))
        self.sort_combo = ComboBox()
        self.sort_combo.addItem("По умолчанию", "")
        self.sort_combo.addItem("Количество ↑", "asc")
        self.sort_combo.addItem("Количество ↓", "desc")
        self.sort_combo.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.sort_combo)

        filter_layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        return filter_panel

    def _apply_filters(self):
        """Применяет фильтры и обновляет список"""
        self.filter = self.supplier_filter.currentData()
        self.search = self.search_input.text()
        self.sort = self.sort_combo.currentData()
        self._update_scroll_list()

    def _open_good_window(self, pk: int, new: bool = False):
        self.app.show_good_window(pk, new)
        self.close()
        print(f"INFO: open {pk} good")

    def show(self):
        self._update_content()
        super().show()
