import datetime
import os
import shutil

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QFileDialog, QMessageBox

from app.entity.user import Role
from app.interface.button import Button
from app.interface.form import FormInput
from app.interface.input import InputText, InputNumber, InputInteger, ComboBox
from app.interface.label import Label
from app.repo.db_session import DBSession
from app.repo.good import GoodRepo, GoodNotFoundError
from app.session.session import session
from app.window.base import BaseWindowWithNavbar
from config.config import DEFAULT_WINDOW_TITLE, MEDIA_PREFIX, DEFAULT_PHOTO_PATH


class GoodWindow(BaseWindowWithNavbar):
    __mode_view = ""
    __mode_edit = "edit"
    __mode_new = "new"

    def __init__(self, app): # app: Application
        super().__init__(app, f"{DEFAULT_WINDOW_TITLE} | Товар")

        self.good_repo = GoodRepo(DBSession())
        self.current_pk = 0
        self.photo_path = DEFAULT_PHOTO_PATH
        self.mode = self.__mode_view

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
        self._set_view_mode()

    def _get_good(self) -> dict:
        """Получает товар из БД"""
        if self.current_pk == 0:
            return self.good_repo.get_default()

        try:
            good = self.good_repo.get_by_id(self.current_pk)
            self.photo_path = good.get("photo")
            return good
        except GoodNotFoundError as err:
            self.status_bar.error(str(err))
            return self.good_repo.get_default()
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Упс.. Неизвестная ошибка")
            return self.good_repo.get_default()

    def _create_combos(self):
        self.cat_combo = ComboBox()
        categories = self.good_repo.get_all_good_categories()
        self.cat_combo.addItem("-- Выберите --", None)
        for category in categories:
            self.cat_combo.addItem(category["name"], category["id"])

        self.unit_combo = ComboBox()
        units = self.good_repo.get_all_measurement_units()
        self.unit_combo.addItem("-- Выберите --", None)
        for unit in units:
            self.unit_combo.addItem(unit["name"], unit["id"])

        self.supplier_combo = ComboBox()
        sups = self.good_repo.get_all_suppliers()
        self.supplier_combo.addItem("-- Выберите --", None)
        for sup in sups:
            self.supplier_combo.addItem(sup["title"], sup["id"])

        self.producer_combo = ComboBox()
        prods = self.good_repo.get_all_producers()
        self.producer_combo.addItem("-- Выберите --", None)
        for prod in prods:
            self.producer_combo.addItem(prod["title"], prod["id"])

        if self.mode == self.__mode_view:
            self.cat_combo.setDisabled(True)
            self.unit_combo.setDisabled(True)
            self.supplier_combo.setDisabled(True)
            self.producer_combo.setDisabled(True)

    def _update_content(self, good: dict):
        """Обновляет содержимое окна с данными товара"""

        self._create_combos()
        readonly = self.mode == self.__mode_view
        required = self.mode != self.__mode_view

        old_widget = self.good_widget
        self.good_widget = QWidget()

        # left side
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(300, 300)
        self.photo_label.setScaledContents(True)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_path = MEDIA_PREFIX + good.get("photo")
        pixmap = QPixmap(photo_path)
        if pixmap.isNull():
            self.status_bar.warn("Изображение не найдено. Попробуйте загрузить новое")
            pixmap = QPixmap(MEDIA_PREFIX+DEFAULT_PHOTO_PATH)
        self.photo_label.setPixmap(pixmap)

        if not readonly:
            self.photo_label.mousePressEvent = self._on_photo_click
            self.photo_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.photo_label.setToolTip("Кликните, чтобы выбрать изображение")
        else:
            self.photo_label.mousePressEvent = None
            self.photo_label.setCursor(Qt.CursorShape.ArrowCursor)
            self.photo_label.setToolTip("")

        # middle
        good_id = Label(f"ID товара: {good.get("id")}")
        cat_title = QHBoxLayout()
        self.cat_combo.select(good.get("category"))
        cat_title.addWidget(self.cat_combo)
        self.title_input = InputText(text=good.get("title"), readonly=readonly)
        cat_title.addWidget(self.title_input)
        cat_title.setAlignment(Qt.AlignmentFlag.AlignJustify)

        self.article_input = InputText(text=good.get("article"), readonly=readonly)
        article = FormInput(
            Label("Артикул"),
            self.article_input,
            required,
        )
        self.desc_input = InputText(text=good.get("description"), readonly=readonly)
        description = FormInput(
            Label("Описание товара"),
            self.desc_input,
            required,
        )
        self.producer_combo.select(good.get("producer"))
        producer = FormInput(
            Label("Производитель"),
            self.producer_combo,
            required,
        )
        self.supplier_combo.select(good.get("supplier"))
        supplier = FormInput(
            Label("Поставщик"),
            self.supplier_combo,
            required,
        )
        self.price_input = InputNumber(value=good.get("price"), minimum=0, readonly=readonly)
        price = FormInput(
            Label("Цена, ₽"),
            self.price_input,
        )
        self.unit_combo.select(good.get("measurement_unit"))
        measurement_unit = FormInput(
            Label("Единица измерения"),
            self.unit_combo,
            required,
        )
        self.amount_input = InputNumber(value=good.get("amount"), minimum=0, readonly=readonly)
        amount = FormInput(
            Label("Количество на складе"),
            self.amount_input,
        )
        info = QVBoxLayout()
        # show ID in edit mode only
        if self.mode == self.__mode_edit:
            info.addWidget(good_id)
        info.addLayout(cat_title)
        info.addLayout(article)
        info.addLayout(description)
        info.addLayout(producer)
        info.addLayout(supplier)
        info.addLayout(price)
        info.addLayout(measurement_unit)
        info.addLayout(amount)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.mode == self.__mode_edit:
            submit_btn = Button("Сохранить")
            submit_btn.on_click(self._save)
            info.addWidget(submit_btn)

            self.delete_btn = Button("Удалить")
            self.delete_btn.on_click(self._delete)
            info.addWidget(self.delete_btn)

        elif self.mode == self.__mode_new:
            submit_btn = Button("Создать")
            submit_btn.on_click(self._create)
            info.addWidget(submit_btn)

        # right side
        self.discount_input = InputInteger(value=good.get("discount"), readonly=readonly)
        discount = FormInput(
            Label("Действующая скидка, %"),
            self.discount_input,
            required,
        )
        discount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create new layout
        layout = QHBoxLayout(self.good_widget)
        layout.setSpacing(15)
        layout.addWidget(self.photo_label)
        layout.addLayout(info)
        layout.addLayout(discount)

        central_widget = self.centralWidget()
        central_layout = central_widget.layout()
        central_layout.replaceWidget(old_widget, self.good_widget)
        old_widget.deleteLater()

    def _on_photo_click(self, event):
        if self.mode == self.__mode_view:
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self._save_photo(file_path)

    def _save_photo(self, source_path: str):
        """Сохраняет фото в медиа-папку и обновляет превью"""

        extension = os.path.splitext(source_path)[1].lower()
        old_photo = self.photo_path
        self.photo_path = f"{int(datetime.datetime.now().timestamp() * 1000)}{extension}"
        filepath = MEDIA_PREFIX+self.photo_path

        try:
            self._delete_photo(old_photo)
            shutil.copy2(source_path, filepath)

            # instantly update in edit mode
            if self.mode == self.__mode_edit:
                self.good_repo.update(self.current_pk, {"photo": self.photo_path})

        except Exception as err:
            print(f"ERROR: Failed to save photo: {err}")
            self.status_bar.error("Ошибка при загрузке изображения")

        pixmap = QPixmap(filepath)
        if not pixmap.isNull():
            if self.mode == self.__mode_new:
                self.status_bar.info("Изображение успешно загружено. Сохраните для применения изменений")
            else:
                self.status_bar.info("Изображение успешно обновлено")
            print(f"INFO: Photo saved as {filepath}")
        else:
            self.status_bar.warn("Не удалось загрузить изображение. Попробуйте ещё раз")
            pixmap = QPixmap(MEDIA_PREFIX + DEFAULT_PHOTO_PATH)
        pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self.photo_label.setPixmap(pixmap)
        self.photo_label.setText("")

    @staticmethod
    def _delete_photo(old_photo: str):
        if old_photo == DEFAULT_PHOTO_PATH:
            return
        try:
            os.remove(MEDIA_PREFIX+old_photo)
            print(f"INFO: delete {old_photo}")
        except Exception as err:
            print(f"ERROR: delete {old_photo}: {err}")

    def _collect_data(self):
        return {
            "article": self.article_input.data,
            "title": self.title_input.data,
            "measurement_unit_id": self.unit_combo.data,
            "price": self.price_input.data,
            "supplier_id": self.supplier_combo.data,
            "producer_id": self.producer_combo.data,
            "good_category_id": self.cat_combo.data,
            "discount": self.discount_input.data,
            "amount": self.amount_input.data,
            "description": self.desc_input.data,
            "photo": self.photo_path,
        }

    def _create(self):
        data = self._collect_data()
        try:
            new_good = self.good_repo.create(data)
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Ошибка при сохранении товара")
            return

        self.current_pk = new_good.get("id")
        self.status_bar.info("Товар успешно создан")
        self._set_edit_mode()

    def _save(self):
        data = self._collect_data()
        try:
            self.good_repo.update(self.current_pk, data)
            self.status_bar.info("Товар успешно обновлён")
        except GoodNotFoundError as err:
            self.status_bar.error(str(err))
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Ошибка при сохранении товара")

    def _delete(self):
        """Удаляет товар с подтверждением"""

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить товар?\n\n"
            f"ID: {self.current_pk}\n"
            f"Название: {self.title_input.data}\n\n"
            f"Это действие необратимо!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        try:
            self.good_repo.delete(self.current_pk)
            self._open_good_list_window()
        except Exception as err:
            print("ERROR:", err)
            self.status_bar.error("Ошибка при удалении товара")

    def _set_view_mode(self):
        self.mode = self.__mode_view
        self.photo_path = DEFAULT_PHOTO_PATH
        self._update_content(self._get_good())

    def _set_edit_mode(self):
        self.mode = self.__mode_edit
        self.photo_path = DEFAULT_PHOTO_PATH
        self._update_content(self._get_good())

    def _set_new_mode(self):
        self.mode = self.__mode_new
        self.photo_path = DEFAULT_PHOTO_PATH
        self._update_content(self._get_good())

    def show(self, pk: int = 0, new: bool = False):
        self.current_pk = pk
        if new:
            self._set_new_mode()
        elif not new and session.user and session.user.get("role") == Role.admin:
            self._set_edit_mode()
        else:
            self._set_view_mode()
        super().show()

    def _open_good_list_window(self):
        self.app.show_good_list_window()
        self.close()
