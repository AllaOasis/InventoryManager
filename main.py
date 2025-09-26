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
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from Modules.InventoryApp import InventoryApp

def load_language() -> str:
    CONFIG_FILE = Path("data/config.json")
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("language", "en")
    return "en"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp(lang=load_language())
    window.show()
    sys.exit(app.exec())