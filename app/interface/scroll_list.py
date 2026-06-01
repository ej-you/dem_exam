from collections.abc import Callable
from typing import List

from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem

from app.interface.button import Button


class ScrollList(QVBoxLayout):
    def __init__(self, header_labels: list, data_keys: list, data: List[dict], on_click_handler: Callable):
        super().__init__()

        self.on_click_handler = on_click_handler

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(len(header_labels)+1)
        header_labels.append("") # for buttons
        self.table.setHorizontalHeaderLabels(header_labels)

        # table settings
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # stretch columns
        header = self.table.horizontalHeader()
        for column in range(len(header_labels)+1):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)

        self.addWidget(self.table)

        self.table.setRowCount(len(data))
        for row, elem in enumerate(data):
            for idx in range(len(data_keys)):
                self.table.setItem(row, idx, QTableWidgetItem(
                    elem.get(data_keys[idx])
                ))

            btn = Button("Подробнее")
            btn.on_click(lambda _, pk=elem.get("id"): self.on_click_handler(pk))
            self.table.setCellWidget(row, len(data_keys), btn)
