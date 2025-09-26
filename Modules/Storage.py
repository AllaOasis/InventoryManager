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

import csv
from pathlib import Path

class Storage:
    @staticmethod
    def save(data,  FILE: Path = None):
        """Save the current data (list of tuples) to CSV."""
        FILE = FILE or Path("data/inventory.csv")

        # Ensure the parent folder exists
        FILE.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with FILE.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Code", "Quantity"])  # Header
                writer.writerows(data)
            print(f"Data saved to {FILE}")
        except Exception as e:
            print(f"Error saving file: {e}")

    @staticmethod
    def open( FILE: Path = None):
        FILE = FILE or Path("data/inventory.csv")
        """Load data from CSV, return as list of tuples."""
        if not FILE.exists():
            print(f"No file found: {FILE}, starting empty.")
            return []

        try:
            with FILE.open("r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header
                data = [(name, code, qty) for name, code, qty in reader]
            print(f"Data loaded from {FILE}")
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
