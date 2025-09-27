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
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout, 
    QFormLayout,
    QLabel, 
    QLineEdit, 
    QSpinBox, 
    QComboBox, 
    QPushButton,
)

from ..Logger import Logger
from ..Storage import Storage
from ..WidgetStyle import WidgetStyle

class EditItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Localization
        self.t = parent.t

        self.setWindowTitle(self.t["edit_item_title"])
        self.resize(400, 200)
        WidgetStyle.setDefaultStyle(self)

        self.parent_app = parent

        # --- Item Selector ---
        self.item_selector = QComboBox(self)
        WidgetStyle.setDefaultStyle(self.item_selector)
        self.item_selector.setStyleSheet(WidgetStyle.comboBoxDefault)
        self.item_selector.addItem(f"-- {self.t['select_item']} --")
        if self.parent_app:
            for name, code, qty in self.parent_app.data:
                self.item_selector.addItem(f"{name} ({code})", (name, code, qty))

        self.item_selector.currentIndexChanged.connect(self.load_item_data)

        # --- Input Fields ---
        self.name_input = QLineEdit()
        WidgetStyle.setDefaultStyle(self.name_input)

        self.code_input = QLineEdit()
        WidgetStyle.setDefaultStyle(self.code_input)

        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(0)
        self.qty_input.setMaximum(999999)
        WidgetStyle.setDefaultStyle(self.qty_input)

        # --- Labels ---
        name_label = QLabel(f"{self.t['name']}:")
        WidgetStyle.setDefaultStyle(name_label)
        code_label = QLabel(f"{self.t['code']}:")
        WidgetStyle.setDefaultStyle(code_label)
        qty_label = QLabel(f"{self.t['quantity']}:")
        WidgetStyle.setDefaultStyle(qty_label)

        # --- Form Layout ---
        form_layout = QFormLayout()
        form_layout.addRow(QLabel(f"{self.t['select_item']}:"),
                           self.item_selector)
        form_layout.addRow(name_label, self.name_input)
        form_layout.addRow(code_label, self.code_input)
        form_layout.addRow(qty_label, self.qty_input)

        # --- Buttons ---
        confirm_button = QPushButton(self.t["confirm"])
        WidgetStyle.setDefaultStyle(confirm_button)
        cancel_button = QPushButton(self.t["cancel"])
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

    def load_item_data(self, index):
        """Fill input fields based on selected item."""
        if index == 0:
            self.name_input.clear()
            self.code_input.clear()
            self.qty_input.setValue(0)
            return

        data = self.item_selector.itemData(index)
        name, code, qty = data
        self.name_input.setText(name)
        self.code_input.setText(code)
        self.qty_input.setValue(int(qty))

    def on_confirm(self):
        """Save changes to the selected item."""
        index = self.item_selector.currentIndex()
        if index == 0:
            self.feedback_label.setText(self.t["select_feedback"])
            return

        new_name = self.name_input.text().strip()
        new_code = self.code_input.text().strip()
        new_qty = self.qty_input.value()

        if not new_name:
            WidgetStyle.setErrorStyle(self.name_input)
            self.feedback_label.setText(self.t["name_empty"])
            return
        else:
            WidgetStyle.setDefaultStyle(self.name_input)

        if not new_code:
            WidgetStyle.setErrorStyle(self.code_input)
            self.feedback_label.setText(self.t["code_empty"])
            return
        else:
            WidgetStyle.setDefaultStyle(self.code_input)

        # Update parent data
        old_data = self.item_selector.itemData(index)
        old_name, old_code, old_qty = old_data

        if self.parent_app:
            for i, (name, code, qty) in enumerate(self.parent_app.data):
                if code == old_code:
                    self.parent_app.data[i] = (new_name, new_code, str(new_qty))
                    from Modules.Logger import Logger
                    from Modules.Storage import Storage
                    Logger.log(self.t["item_updated"].format(name=new_name, code=new_code, qty=new_qty))
                    self.parent_app.load_logs()
                    self.parent_app.populate_table(self.parent_app.data)
                    Storage.save(self.parent_app.data)
                    break

        self.feedback_label.setText(self.t["name_updated"].format(new_name=new_name, new_code=new_code))
        self.accept()
