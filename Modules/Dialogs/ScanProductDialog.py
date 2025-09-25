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

from PyQt6.QtCore import Qt
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

class ScanProductDialog(QDialog):
    def __init__(self, parent=None, table=None):
        super().__init__(parent)
        self.setWindowTitle("Scan Products")
        self.resize(350, 180)
        WidgetStyle.setDefaultStyle(self)

        self.table = table  # reference to the table
        self.parent_ref = parent  # keep a reference to parent for data

        # --- Inputs ---
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setValue(1)
        self.quantity_input.setFixedWidth(80)
        self.quantity_input.setStyleSheet(WidgetStyle.spinboxDefault)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Scan or type product code...")
        WidgetStyle.setDefaultStyle(self.code_input)

        self.feedback_label = QLabel("")
        WidgetStyle.setDefaultStyle(self.feedback_label)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Buttons ---
        confirm_button = QPushButton("Confirm")
        WidgetStyle.setDefaultStyle(confirm_button)
        cancel_button = QPushButton("Cancel")
        WidgetStyle.setDefaultStyle(cancel_button)

        confirm_button.clicked.connect(self.on_confirm)
        cancel_button.clicked.connect(self.reject)

        # --- Layout ---
        form_layout = QFormLayout()
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Product Code:", self.code_input)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        button_layout.setSpacing(15)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.feedback_label)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(main_layout)

        # --- Center dialog over parent ---
        if parent:
            parent_rect = parent.frameGeometry()
            dialog_rect = self.frameGeometry()
            dialog_rect.moveCenter(parent_rect.center())
            self.move(dialog_rect.topLeft())

        # Focus on code input by default
        self.code_input.setFocus()

    def on_confirm(self):
        code = self.code_input.text().strip()
        qty = self.quantity_input.value()

        if not code:
            self.feedback_label.setText("Please enter a product code!")
            return

        found = False
        for i, (name, item_code, current_qty) in enumerate(self.parent_ref.data):
            if item_code == code:
                new_qty = int(current_qty) + qty
                self.parent_ref.data[i] = (name, item_code, str(new_qty))
                self.feedback_label.setText(f"Updated '{name}' → {new_qty}")
                found = True
                break

        if not found:
            self.feedback_label.setText(f"Product code '{code}' not found!")

        # Refresh table
        self.parent_ref.populate_table(self.parent_ref.data)

        # Clear code input for next scan
        self.code_input.clear()
        self.code_input.setFocus()
