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

from PyQt6.QtWidgets import  (
    QLineEdit, 
    QVBoxLayout, 
    QLabel, 
    QDialog, 
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QSpinBox,
)

from ..WidgetStyle import WidgetStyle

class AddItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Localization
        self.t = parent.t

        self.setWindowTitle(self.t["add_item_title"])
        self.resize(350, 180)
        WidgetStyle.setDefaultStyle(self)

        # --- Inputs ---
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText(self.t["name"])
        WidgetStyle.setDefaultStyle(self.name_input)

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText(self.t["code"])
        WidgetStyle.setDefaultStyle(self.code_input)

        self.qty_input = QSpinBox(self)
        self.qty_input.setMinimum(0)
        self.qty_input.setValue(0)
        self.qty_input.setMaximum(999999)
        WidgetStyle.setDefaultStyle(self.qty_input)

        # Labels
        name_label = QLabel(f"{self.t['name']}:", self)
        WidgetStyle.setDefaultStyle(name_label)
        code_label = QLabel(f"{self.t['code']}:", self)
        WidgetStyle.setDefaultStyle(code_label)
        qty_label = QLabel(f"{self.t['quantity']}:", self)
        WidgetStyle.setDefaultStyle(qty_label)

        # --- Form Layout ---
        form_layout = QFormLayout()
        form_layout.addRow(name_label, self.name_input)
        form_layout.addRow(code_label, self.code_input)
        form_layout.addRow(qty_label, self.qty_input)

        # --- Buttons ---
        confirm_button = QPushButton(self.t["confirm"], self)
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

    def on_confirm(self):
        """Validate inputs and add item through parent."""
        name = self.name_input.text().strip()
        code = self.code_input.text().strip()
        qty = self.qty_input.value()

        # Validation
        if not name:
            WidgetStyle.setErrorStyle(self.name_input)
            self.feedback_label.setText(self.t["enter_name_feedback"])
            return
        else:
            WidgetStyle.setDefaultStyle(self.name_input)

        if not code:
            WidgetStyle.setErrorStyle(self.code_input)
            self.feedback_label.setText(self.t["enter_code_feedback"])
            return
        else:
            WidgetStyle.setDefaultStyle(self.code_input)

        # --- Call parent's add_data_row ---
        if self.parent() and hasattr(self.parent(), "add_data_row"):
            self.parent().add_data_row(name, code, qty)
            self.feedback_label.setText(self.t["added_feedback"].format(name=name, code=code, qty=qty))
            self.accept()
        else:
            self.feedback_label.setText("Error: Parent does not support add_data_row.")
