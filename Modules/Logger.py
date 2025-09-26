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
from datetime import datetime

class Logger:
    @staticmethod
    def log(message: str, FILE: Path = None):
        FILE = FILE or Path("data/inventory.log")

        # Ensure the parent folder exists
        FILE.parent.mkdir(parents=True, exist_ok=True)

        try:
            with FILE.open("a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                timestamp = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                writer.writerow([timestamp, message])
            print(f"LOG: {message}")  # still echo to console
        except Exception as e:
            print(f"Error writing log: {e}")

    @staticmethod
    def read(FILE: Path = None):
        FILE = FILE or Path("data/inventory.log")

        if not FILE.exists():
            print(f"No log file found: {FILE}")
            return []

        try:
            with FILE.open("r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                return [(timestamp, message) for timestamp, message in reader]
        except Exception as e:
            print(f"Error reading log: {e}")
            return []
