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
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QDialog,
    QSpinBox,
)

from ..WidgetStyle import WidgetStyle

from ..WidgetStyle import WidgetStyle
from ..Localization import translations
from ..SQLManager import SQLManager

class DatabaseConfigDialog(QDialog):
    def __init__(self, parent=None, lang="en"):
        super().__init__(parent)

        self.lang = parent.lang
        self.t = translations[self.lang]  # fallback to English

        self.setWindowTitle(self.t["titleDB"])
        self.setFixedSize(360, 240)

        # --- Inputs ---
        self.host_input = QLineEdit(self)
        self.port_input = QSpinBox(self)
        self.port_input.setRange(0, 65535)
        self.port_input.setValue(3306)
        self.port_input.setFixedWidth(100)

        self.db_input = QLineEdit(self)
        self.user_input = QLineEdit(self)
        self.pass_input = QLineEdit(self)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        for widget in (self.host_input, self.port_input, self.db_input, self.user_input, self.pass_input):
            WidgetStyle.setDefaultStyle(widget)

        # --- Labels ---
        host_label = QLabel(self.t["host"])
        db_label = QLabel(self.t["database"])
        user_label = QLabel(self.t["username"])
        pass_label = QLabel(self.t["password"])

        for lbl in (host_label, db_label, user_label, pass_label):
            WidgetStyle.setDefaultStyle(lbl)

        # --- Form Layout ---
        form_layout = QFormLayout()

        host_port_layout = QHBoxLayout()
        host_port_layout.addWidget(self.host_input)
        host_port_layout.addWidget(QLabel(":"))
        host_port_layout.addWidget(self.port_input)

        form_layout.addRow(host_label, host_port_layout)
        form_layout.addRow(db_label, self.db_input)
        form_layout.addRow(user_label, self.user_input)
        form_layout.addRow(pass_label, self.pass_input)

        # --- Buttons ---
        confirm_button = QPushButton(self.t["save"])
        WidgetStyle.setDefaultStyle(confirm_button)

        test_button = QPushButton(self.t["test_connection"])
        WidgetStyle.setDefaultStyle(test_button)

        cancel_button = QPushButton(self.t["cancel"])
        WidgetStyle.setDefaultStyle(cancel_button)

        confirm_button.clicked.connect(self.on_confirm)
        test_button.clicked.connect(self.on_test)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(test_button)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        # --- Feedback Label ---
        self.feedback_label = QLabel(self.t["feedback_empty"])
        self.feedback_label.setWordWrap(True)
        WidgetStyle.setDefaultStyle(self.feedback_label)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.feedback_label)

        self.setLayout(main_layout)

    def on_confirm(self):
        """Return entered database info to parent."""
        
        SQLManager.save_config("host", self.host_input.text().strip())
        SQLManager.save_config("database", self.db_input.text().strip())
        SQLManager.save_config("user", self.db_input.text().strip())
        SQLManager.save_config("password", self.pass_input.text().strip())
        SQLManager.save_config("port", self.port_input.text().strip())

        SQLManager.singleton().config_connect()

        # You’ll add saving logic here
        self.accept()

    def on_test(self):
        """Dummy connection test (you already handle real checks)."""
        self.feedback_label.setText("Checking...")
        
        if not self.host_input.text() or not self.db_input.text():
            self.feedback_label.setText("Please enter host and database first.")
            return

        # Simulate quick check
        if SQLManager.connection_test(
            self.host_input.text().strip(), 
            self.user_input.text().strip(),
            self.pass_input.text().strip(),
            self.db_input.text().strip(),
            self.port_input.value()
        ): self.feedback_label.setText("Connection test successful.")
        else: self.feedback_label.setText("Connection test Failed.")