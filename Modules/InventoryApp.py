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

import json
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import  (
    QMainWindow, 
    QLineEdit, 
    QVBoxLayout, 
    QWidget, 
    QLabel, 
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QStackedLayout
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from pathlib import Path
from Modules.Logger import Logger
from Modules.Storage import Storage
from Modules.Localization import translations
from Modules.WidgetStyle import WidgetStyle
from Modules.Dialogs.AddItemDialog import AddItemDialog
from Modules.Dialogs.EditItemDialog import EditItemDialog
from Modules.Dialogs.RemoveItemDialog import RemoveItemDialog
from Modules.Dialogs.ScanProductDialog import ScanProductDialog


class InventoryApp(QMainWindow):
    def __init__(self, lang="en"):
        """Create and set up the Application Window."""
        super().__init__()

        # Localization
        self.lang = lang
        self.t = translations[self.lang]

        self.setWindowTitle(self.t["app_name"])
        self.resize(800, 500)
        WidgetStyle.setDefaultStyle(self)

        self.data = []
        self.all_logs = []

        self.init_ui()
        self.init_datatable()
        self.init_stacked_views()  # stacked layout for inventory, logs

    # -------------------------
    # UI Initialization
    # -------------------------
    def init_ui(self):
        """Add components to the Application Window."""
        self.init_menu_bar()

    def init_menu_bar(self):
        """Generate the menu bar with multi-language support."""
        menubar = self.menuBar()
        WidgetStyle.setDefaultStyle(menubar)

        # Home Button
        self.home_action = QAction(self.t["home"], self)
        self.home_action.triggered.connect(self.show_welcome_view)
        menubar.addAction(self.home_action)

        # Inventory menu
        self.inventory_menu = menubar.addMenu(self.t["inventory"])
        self.add_item_action = QAction(self.t["add_item"], self)
        self.add_item_action.triggered.connect(self.add_item_dialog)
        self.edit_item_action = QAction(self.t["edit_item"], self)
        self.edit_item_action.triggered.connect(self.edit_item_dialog)
        self.remove_item_action = QAction(self.t["remove_item"], self)
        self.remove_item_action.triggered.connect(self.remove_item_dialog)
        self.view_all_action = QAction(self.t["view_all"], self)
        self.view_all_action.triggered.connect(self.show_inventory_view)

        self.inventory_menu.addAction(self.add_item_action)
        self.inventory_menu.addAction(self.edit_item_action)
        self.inventory_menu.addAction(self.remove_item_action)
        self.inventory_menu.addAction(self.view_all_action)

        # Logs menu
        self.view_logs_action = QAction(self.t["logs"], self)
        self.view_logs_action.triggered.connect(self.show_log_view)
        menubar.addAction(self.view_logs_action)

        # Settings menu
        self.settings_menu = menubar.addMenu(self.t["settings"])
        self.language_menu = self.settings_menu.addMenu(self.t["language"])
        self.slovene = QAction(self.t["si"], self)
        self.slovene.triggered.connect(self.set_slovenian)
        self.english = QAction(self.t["en"], self)
        self.english.triggered.connect(self.set_english)
        self.language_menu.addAction(self.slovene)
        self.language_menu.addAction(self.english)

        # Credits menu
        self.credits_action = QAction(self.t["credits"], self)
        self.credits_action.triggered.connect(self.show_credits_dialog)
        menubar.addAction(self.credits_action)


    # -------------------------
    # Dialogs
    # -------------------------
    def add_item_dialog(self):
        dialog = AddItemDialog(self)
        dialog.exec()
    
    def remove_item_dialog(self):
        dialog = RemoveItemDialog(self)
        dialog.exec()
    
    def edit_item_dialog(self):
        dialog = EditItemDialog(self)
        dialog.exec()
    
    def scan_product_dialog(self):
        if hasattr(self, 'table') and self.table is not None:
            dialog = ScanProductDialog(parent=self, table=self.table)
            dialog.exec()
        else:
            print("Error: Inventory table not initialized yet!")
    
    def show_credits_dialog(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            self.t["credits"],
            self.t["credits_content"],
        )


    # -------------------------
    # Data / Table Initialization
    # -------------------------
    def init_datatable(self):
        """Create the main inventory table."""
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([self.t["name"], self.t["code"], self.t["quantity"]])
        self.table.setSortingEnabled(True)
        self.get_data()
        self.populate_table(self.data)

    # -------------------------
    # Stacked Layout: Welcome / Inventory / Logs
    # -------------------------

    def init_stacked_views(self):
        """Create stacked layout with Welcome, Inventory, and Log pages."""
        self.central_widget = QWidget()
        self.stacked_layout = QStackedLayout()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        # --- Welcome Page ---
        self.welcome_widget = QWidget()
        welcome_layout = QVBoxLayout()
        self.welcome_widget.setLayout(welcome_layout)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setSpacing(20)

        # Image / Logo
        logo_path = Path("data/logo.png")
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            logo_label = QLabel()
            logo_label.setPixmap(pixmap.scaledToWidth(180, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            welcome_layout.addWidget(logo_label)

        # Welcome text
        self.welcome_label = QLabel(
            f"<h2>{self.t['welcome']}</h2>"
            f"<p style='font-size:14px; color: #555;'>"
            f"{self.t['welcome_subtext']}"
            "</p>"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setWordWrap(True)
        welcome_layout.addWidget(self.welcome_label)

        # Optional navigation buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.inventory_button = QPushButton(self.t["view_all"])
        WidgetStyle.setDefaultStyle(self.inventory_button)
        self.inventory_button.setFixedWidth(150)
        self.inventory_button.clicked.connect(self.show_inventory_view)

        self.logs_button = QPushButton(self.t["logs"])
        WidgetStyle.setDefaultStyle(self.logs_button)
        self.logs_button.setFixedWidth(150)
        self.logs_button.clicked.connect(self.show_log_view)

        button_layout.addWidget(self.inventory_button)
        button_layout.addWidget(self.logs_button)
        welcome_layout.addLayout(button_layout)

        # --- Inventory Page ---
        self.inventory_widget = QWidget()
        inventory_layout = QVBoxLayout()
        self.inventory_widget.setLayout(inventory_layout)

        # Top control row
        control_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.t["search_placeholder"])
        WidgetStyle.setDefaultStyle(self.search_input)

        self.search_button = QPushButton(self.t["search"])
        WidgetStyle.setDefaultStyle(self.search_button)
        self.scan_button = QPushButton(self.t["scan_products"])
        WidgetStyle.setDefaultStyle(self.scan_button)

        control_layout.addWidget(self.search_input)
        control_layout.addWidget(self.search_button)
        control_layout.addWidget(self.scan_button)
        inventory_layout.addLayout(control_layout)

        # Inventory table
        inventory_layout.addWidget(self.table)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        WidgetStyle.setDefaultStyle(self.table)

        # Signals
        self.search_button.clicked.connect(self.search_items)
        self.scan_button.clicked.connect(self.scan_product_dialog)
        self.search_input.returnPressed.connect(self.search_items)
        self.table.itemChanged.connect(self.on_table_item_changed)

        # --- Log Viewer Page ---
        self.log_widget = QWidget()
        log_layout = QVBoxLayout()
        self.log_widget.setLayout(log_layout)

        self.log_search_input = QLineEdit()
        self.log_search_input.setPlaceholderText(self.t["search_placeholder"])
        WidgetStyle.setDefaultStyle(self.log_search_input)

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(2)
        self.log_table.setHorizontalHeaderLabels([self.t["timestamp"], self.t["message"]])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.log_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.log_table.setStyleSheet(WidgetStyle.logTable)

        log_layout.addWidget(self.log_search_input)
        log_layout.addWidget(self.log_table)
        self.log_search_input.textChanged.connect(self.filter_logs)

        # Add pages to stacked layout
        self.stacked_layout.addWidget(self.welcome_widget)
        self.stacked_layout.addWidget(self.inventory_widget)
        self.stacked_layout.addWidget(self.log_widget)

        # Show welcome page by default
        self.stacked_layout.setCurrentWidget(self.welcome_widget)

        # Load logs initially
        self.load_logs()


    # -------------------------
    # Page Switching
    # -------------------------
    def show_welcome_view(self):
        self.stacked_layout.setCurrentWidget(self.welcome_widget)

    def show_inventory_view(self):
        self.stacked_layout.setCurrentWidget(self.inventory_widget)

    def show_log_view(self):
        self.stacked_layout.setCurrentWidget(self.log_widget)

    # -------------------------
    # Data Handling
    # -------------------------
    def get_data(self):
        self.data = Storage.open()

    def populate_table(self, data, location=None):
        if location is None:
            location = self.table
        location.blockSignals(True)
        location.setRowCount(len(data))
        for row, (name, code, qty) in enumerate(data):
            name_item = QTableWidgetItem(name)
            code_item = QTableWidgetItem(code)
            qty_item = QTableWidgetItem(str(qty))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            code_item.setFlags(code_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            location.setItem(row, 0, name_item)
            location.setItem(row, 1, code_item)
            location.setItem(row, 2, qty_item)
        location.blockSignals(False)

    def on_table_item_changed(self, item: QTableWidgetItem):
        row, col = item.row(), item.column()
        if col != 2:
            return
        edited_code = self.table.item(row, 1).text()
        try:
            new_qty = int(item.text())
            if new_qty < 0:
                raise ValueError
        except ValueError:
            old_qty = next(qty for name, code, qty in self.data if code == edited_code)
            self.table.blockSignals(True)
            self.table.item(row, col).setText(str(old_qty))
            self.table.blockSignals(False)
            return
        for i, (name, code, qty) in enumerate(self.data):
            if code == edited_code:
                self.data[i] = (name, code, str(new_qty))
                Logger.log(self.t["product_updated"].format(name=name, qty=new_qty))
                self.load_logs()
                Storage.save(self.data)
                break

    def search_items(self):
        term = self.search_input.text().strip().lower()
        filtered = [item for item in self.data if term in item[0].lower() or term in item[1]]
        self.populate_table(filtered)

    def add_data_row(self, name: str, code: str, qty: int | str = 0):
        row = (name, code, str(qty))
        self.data.append(row)
        Logger.log(self.t["product_added"].format(name=name,code=code, qty=qty))
        self.load_logs()
        Storage.save(self.data)
        self.populate_table(self.data)

    # -------------------------
    # Logs
    # -------------------------
    def load_logs(self):
        self.all_logs = []
        log_file = Path("data/inventory.log")
        if not log_file.exists():
            return
        with log_file.open("r", encoding="utf-8") as f:
            for line in f:
                if "," in line:
                    timestamp, message = line.strip().split(",", 1)
                else:
                    timestamp, message = "Unknown", line.strip()
                self.all_logs.append((timestamp, message))
        self.populate_log_table(self.all_logs)

    def populate_log_table(self, logs):
        self.log_table.blockSignals(True)
        self.log_table.setRowCount(len(logs))
        for row, (timestamp, message) in enumerate(logs):
            self.log_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.log_table.setItem(row, 1, QTableWidgetItem(message))
        self.log_table.blockSignals(False)

    def filter_logs(self, text):
        term = text.strip().lower()
        if not term:
            filtered = self.all_logs
        else:
            filtered = [log for log in self.all_logs if term in log[0].lower() or term in log[1].lower()]
        self.populate_log_table(filtered)

    # -------------------------
    # Language Change
    # -------------------------

    def set_slovenian(self):
        self.lang = "si"
        self.t = translations[self.lang]
        self.refresh_ui_texts()
    
    def set_english(self):
        self.lang = "en"
        self.t = translations[self.lang]
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        """Update all text elements in the main window according to current language."""
        self.setWindowTitle(self.t["app_name"])

        # --- Menu Bar ---
        self.home_action.setText(self.t["home"])
        self.inventory_menu.setTitle(self.t["inventory"])
        self.add_item_action.setText(self.t["add_item"])
        self.edit_item_action.setText(self.t["edit_item"])
        self.remove_item_action.setText(self.t["remove_item"])
        self.view_all_action.setText(self.t["view_all"])
        self.view_logs_action.setText(self.t["logs"])
        self.settings_menu.setTitle(self.t["settings"])
        self.language_menu.setTitle(self.t["language"])
        self.slovene.setText(self.t["si"])
        self.english.setText(self.t["en"])
        self.credits_action.setText(self.t["credits"])

        # --- Welcome Page ---
        self.welcome_label.setText(
            f"<h2>{self.t['welcome']}</h2>"
            f"<p style='font-size:14px; color: #555;'>"
            f"{self.t['welcome_subtext']}"
            "</p>"
        )

        # --- Welcome Page Buttons ---
        # Assuming you kept references for inventory/log buttons:
        self.inventory_button.setText(self.t["view_all"])
        self.logs_button.setText(self.t["logs"])

        # --- Inventory Page ---
        self.search_input.setPlaceholderText(self.t["search_placeholder"])
        self.search_button.setText(self.t["search"])
        self.scan_button.setText(self.t["scan_products"])

        # --- Log Viewer Page ---
        self.log_search_input.setPlaceholderText(self.t["search_placeholder"])
        self.log_table.setHorizontalHeaderLabels([self.t["timestamp"], self.t["message"]])

        # --- Table headers ---
        self.table.setHorizontalHeaderLabels([self.t["name"], self.t["code"], self.t["quantity"]])
        self.save_language()

    def save_language(self):
        CONFIG_FILE = Path("data/config.json")
        CONFIG_FILE.parent.mkdir(exist_ok=True)  # make sure 'data/' exists
        config = {"language": self.lang}
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(config, f)
