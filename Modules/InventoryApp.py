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

import sys
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
)

from Modules.WidgetStyle import WidgetStyle
from Modules.Dialogs.AddItemDialog import AddItemDialog
from Modules.Dialogs.ScanProductDialog import ScanProductDialog

class InventoryApp(QMainWindow):
    def __init__(self):
        """Create and set up the Application Window."""
        super().__init__()

        self.setWindowTitle("Inventory Management System")
        self.resize(600, 400)
        WidgetStyle.setDefaultStyle(self)

        self.init_ui()

        self.init_datatable()

    def init_ui(self):
        """Add components to the Application Window."""
        # Create central widget and layout
        self.init_welcome()

        # Menu bar setup
        self.init_menu_bar()
    
    def init_welcome(self):
        """Generate the initial screen displayed."""
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("Welcome to Inventory Management\n\nApplication still in development", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def init_menu_bar(self):
        """Generate the menu bar."""
        menubar = self.menuBar()
        WidgetStyle.setDefaultStyle(menubar)

        # File menu
        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        new_action.setDisabled(True)
        open_action = QAction("Open", self)
        open_action.setDisabled(True)
        save_action = QAction("Save", self)
        save_action.setDisabled(True)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # Inventory menu
        inventory_menu = menubar.addMenu("Inventory")
        add_item_action = QAction("Add Item", self)
        add_item_action.triggered.connect(self.add_item_dialog)
        edit_item_action = QAction("Edit Item", self)
        remove_item_action = QAction("Remove Item", self)
        view_all_action = QAction("View All Items", self)
        view_all_action.triggered.connect(self.init_item_list)

        inventory_menu.addAction(add_item_action)
        inventory_menu.addAction(edit_item_action)
        inventory_menu.addAction(remove_item_action)
        inventory_menu.addAction(view_all_action)

        # Reports menu
        reports_menu = menubar.addMenu("Reports")
        reports_menu.setDisabled(True)
        generate_report_action = QAction("Generate Report", self)
        view_report_action = QAction("View Report", self)

        reports_menu.addAction(generate_report_action)
        reports_menu.addAction(view_report_action)

        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        settings_menu.setDisabled(True)
        preferences_action = QAction("Preferences", self)
        backup_action = QAction("Backup", self)

        settings_menu.addAction(preferences_action)
        settings_menu.addAction(backup_action)
        
    def add_item_dialog(self):
        dialog = AddItemDialog(self)
        dialog.exec()  # This opens the dialog and blocks further interaction until closed

    def init_datatable(self):
        # --- Items Table --- 
        self.table = QTableWidget() 
        self.table.setColumnCount(3) 
        # Example: Name, Code, Quantity 
        self.table.setHorizontalHeaderLabels(["Name", "Code", "Quantity"])
        self.table.setSortingEnabled(True)

        self.get_data()

        self.populate_table(self.data)

    def init_item_list(self):
        """Generate the Items List page with Search and Scan functionality."""
    
        central_widget = QWidget()
        main_layout = QVBoxLayout()
    
        # --- Top Control Row ---
        control_layout = QHBoxLayout()
    
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search items by name or code...")
        WidgetStyle.setDefaultStyle(self.search_input)
    
        search_button = QPushButton("Search")
        WidgetStyle.setDefaultStyle(search_button)
    
        scan_button = QPushButton("Scan Products")
        WidgetStyle.setDefaultStyle(scan_button)
    
        control_layout.addWidget(self.search_input)
        control_layout.addWidget(search_button)
        control_layout.addWidget(scan_button)
    
        main_layout.addLayout(control_layout)
    
        # Stretch headers
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Refresh the table on load
        self.populate_table(self.data)

        # Apply table style
        WidgetStyle.setDefaultStyle(self.table)
    
        main_layout.addWidget(self.table)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
        # --- Signals ---
        search_button.clicked.connect(self.search_items)
        scan_button.clicked.connect(self.open_scanning_dialog)
        self.search_input.returnPressed.connect(self.search_items)
        self.table.itemChanged.connect(self.on_table_item_changed)
    
    # -----------------------
    # Helper functions
    # -----------------------
    
    def populate_table(self, data, location=None):
        """Fill the table with provided data."""
        if location is None:
            location = self.table

        location.blockSignals(True)
        location.setRowCount(len(data))
        for row, (name, code, qty) in enumerate(data):
            name_item = QTableWidgetItem(name)
            code_item = QTableWidgetItem(code)
            qty_item = QTableWidgetItem(str(qty))

            # Disable editing for Name and Code
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            code_item.setFlags(code_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            # Quantity remains editable (default flags)
            
            location.setItem(row, 0, name_item)
            location.setItem(row, 1, code_item)
            location.setItem(row, 2, qty_item)
        location.blockSignals(False)

    def on_table_item_changed(self, item: QTableWidgetItem):
        """Update self.data when the table is edited manually, safe for filtered views."""
        row = item.row()
        col = item.column()

        # Only allow editing Quantity (column 2)
        if col != 2:
            return

        # Get the product code of the edited row in the table
        edited_code = self.table.item(row, 1).text()
        new_value = item.text()

        # Validate the input is an integer
        try:
            new_qty = int(new_value)
            if new_qty < 0:
                raise ValueError
        except ValueError:
            # Revert invalid input
            old_qty = next(qty for name, code, qty in self.data if code == edited_code)
            self.table.blockSignals(True)
            self.table.item(row, col).setText(str(old_qty))
            self.table.blockSignals(False)
            return

        # Find the matching row in the original data by code
        for i, (name, code, qty) in enumerate(self.data):
            if code == edited_code:
                self.data[i] = (name, code, str(new_qty))
                print(f"Updated {edited_code} quantity → {new_qty}")
                break



    def search_items(self):
        """Filter table based on search input."""
        term = self.search_input.text().strip().lower()
        filtered = [item for item in self.data if term in item[0].lower() or term in item[1]]
        self.populate_table(filtered)

    def open_scanning_dialog(self):
        if hasattr(self, 'table') and self.table is not None:
            dialog = ScanProductDialog(parent=self, table=self.table)
            dialog.exec()
        else:
            print("Error: Inventory table not initialized yet!")

    def get_data(self):
        # Demo data
        demo_data = [
            ("Screwdriver", "001", "15"),
            ("Wrench", "002", "8"),
            ("Hammer", "003", "5"),
            ("Drill", "004", "12"),
            ("Pliers", "005", "20")
        ]
        self.data = demo_data
    
    def add_data_row(self, name: str, code: str, qty: int | str = 0):
        """Add a new row to the data and refresh the table."""
        # Ensure qty is stored as a string for consistency with self.data
        row = (name, code, str(qty))
        
        # Append to the data list
        self.data.append(row)
        
        # Refresh table
        self.populate_table(self.data)
