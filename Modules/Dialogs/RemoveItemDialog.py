# Inventory Management Application - A Python-based inventory management system using PyQt6
# Copyright (C) 2025 Lackovič Aljaž
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See <https://www.gnu.org/licenses/> for more details.
#
# Dependencies:
#  - PyQt6 (GPLv3) for the graphical user interface


from PyQt6.QtWidgets import (
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QDialog,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QComboBox,
)
from ..WidgetStyle import WidgetStyle

class RemoveItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Localization
        self.t = parent.t

        self.setWindowTitle(self.t["remove_item_title"])
        self.resize(350, 150)
        WidgetStyle.setDefaultStyle(self)

        self.parent_app = parent

        # --- Inputs ---
        self.item_selector = QComboBox(self)
        self.populate_items()
        WidgetStyle.setDefaultStyle(self.item_selector)

        self.confirm_code_input = QLineEdit(self)
        self.confirm_code_input.setPlaceholderText(self.t["placeholder_code"])
        WidgetStyle.setDefaultStyle(self.confirm_code_input)

        # Labels
        item_label = QLabel(f"{self.t['select_item']}:", self)
        WidgetStyle.setDefaultStyle(item_label)
        code_label = QLabel(f"{self.t['confirm_code']}:", self)
        WidgetStyle.setDefaultStyle(code_label)

        # --- Form Layout ---
        form_layout = QFormLayout()
        form_layout.addRow(item_label, self.item_selector)
        form_layout.addRow(code_label, self.confirm_code_input)

        # --- Buttons ---
        confirm_button = QPushButton(self.t["confirm_removal"], self)
        WidgetStyle.setDefaultStyle(confirm_button)
        cancel_button = QPushButton(self.t["cancel"], self)
        WidgetStyle.setDefaultStyle(cancel_button)

        confirm_button.clicked.connect(self.on_confirm)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        # --- Feedback Label ---
        self.feedback_label = QLabel("")
        WidgetStyle.setDefaultStyle(self.feedback_label)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.feedback_label)

        self.setLayout(main_layout)

    def populate_items(self):
        """Populate combo box with current items in the format Name(Code)."""
        self.item_selector.clear()
        self.item_selector.addItem(self.t["select_placeholder"])
        if self.parent_app and hasattr(self.parent_app, "data"):
            for name, code, qty in self.parent_app.data:
                self.item_selector.addItem(f"{name} ({code})", code)

    def on_confirm(self):
        """Remove the selected item if code matches confirmation input."""
        selected_index = self.item_selector.currentIndex()
        selected_code = self.item_selector.itemData(selected_index)
        confirm_code = self.confirm_code_input.text().strip()

        if confirm_code != selected_code:
            WidgetStyle.setErrorStyle(self.confirm_code_input)
            self.feedback_label.setText(self.t["enter_code_feedback"])
            return
        else:
            WidgetStyle.setDefaultStyle(self.confirm_code_input)

        # Remove the item from parent data
        if self.parent_app and hasattr(self.parent_app, "data"):
            self.parent_app.data = [
                (name, code, qty)
                for name, code, qty in self.parent_app.data
                if code != selected_code
            ]

            # Save changes and refresh table
            from Modules.Storage import Storage
            Storage.save(self.parent_app.data)
            self.parent_app.populate_table(self.parent_app.data)

            # Log the removal
            from Modules.Logger import Logger
            Logger.log(f"Removed item: Code {selected_code}")
            self.parent_app.load_logs()

            self.accept()
