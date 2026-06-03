from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from app.interface.button import Button
from app.interface.form import FormInput
from app.interface.input import InputText, InputNumber, InputInteger
from app.interface.label import Label
from app.repo.db_session import DBSession
from app.repo.good import GoodRepo, GoodNotFoundError
from app.window.base import BaseWindowWithNavbar
from config.config import DEFAULT_WINDOW_TITLE, MEDIA_PREFIX, DEFAULT_PHOTO_PATH


class GoodWindow(BaseWindowWithNavbar):
    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Товар")

        self.good_repo = GoodRepo(DBSession())
        self.current_pk = 0

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # back button
        self.back_btn = Button("← Назад к списку")
        self.back_btn.on_click(self._open_good_list_window)
        main_layout.addWidget(self.back_btn)

        # content
        self.good_widget = QWidget()
        main_layout.addWidget(self.good_widget)
        self._update_content(self.good_repo.get_default())

        # TODO: submit button

    def _get_good(self, pk: int) -> dict:
        """Получает товар из БД"""

        try:
            return self.good_repo.get_by_id(pk)
        except GoodNotFoundError as err:
            self.status_bar.error(str(err))
            return self.good_repo.get_default()
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Упс.. Неизвестная ошибка")
            return self.good_repo.get_default()

    def _update_content(self, good: dict):
        """Обновляет содержимое окна с данными товара"""
        old_widget = self.good_widget
        self.good_widget = QWidget()

        # left side
        photo = QLabel()
        photo_path = MEDIA_PREFIX+good.get("photo")
        pixmap = QPixmap(photo_path)
        photo.setPixmap(pixmap)
        photo.setFixedSize(300, 300)
        photo.setScaledContents(True)

        # middle
        good_id = Label(f"ID товара: {good.get("id")}")
        cat_title = QHBoxLayout()
        cat_title.addWidget(InputText(text=good.get("category")))
        cat_title.addWidget(InputText(text=good.get("title")))
        cat_title.setAlignment(Qt.AlignmentFlag.AlignJustify)
        description = FormInput(
            Label("Описание товара"),
            InputText(text=good.get("description")),
        )
        producer = FormInput(
            Label("Производитель"),
            InputText(text=good.get("producer")),
        )
        supplier = FormInput(
            Label("Поставщик"),
            InputText(text=good.get("supplier")),
        )
        price = FormInput(
            Label("Цена, ₽"),
            InputNumber(value=good.get("price"), minimum=0),
        )
        measurement_unit = FormInput(
            Label("Единица измерения"),
            InputText(text=good.get("measurement_unit")),
        )
        amount = FormInput(
            Label("Количество на складе"),
            InputNumber(value=good.get("amount"), minimum=0),
        )
        info = QVBoxLayout()
        info.addWidget(good_id)
        info.addLayout(cat_title)
        info.addLayout(description)
        info.addLayout(producer)
        info.addLayout(supplier)
        info.addLayout(price)
        info.addLayout(measurement_unit)
        info.addLayout(amount)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # right side
        discount_label = Label("Действующая скидка, %")
        discount_input = InputInteger(value=good.get("discount"))
        discount = QVBoxLayout()
        discount.addWidget(discount_label)
        discount.addWidget(discount_input)
        discount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create new layout
        layout = QHBoxLayout(self.good_widget)
        layout.setSpacing(20)
        layout.addWidget(photo)
        layout.addLayout(info)
        layout.addLayout(discount)

        central_widget = self.centralWidget()
        central_layout = central_widget.layout()
        central_layout.replaceWidget(old_widget, self.good_widget)
        old_widget.deleteLater()

    def show(self, pk: int = 0):
        self.current_pk = pk # TODO: need???
        if pk:
            good = self._get_good(pk)
        else:
            good = self.good_repo.get_default()

        self._update_content(good)
        super().show()

    def _open_good_list_window(self):
        self.app.show_good_list_window()
        self.close()
