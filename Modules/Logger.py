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
import json
import base64
from pathlib import Path
from datetime import datetime
from Modules.SQLManager import SQLManager

class Logger:
    @staticmethod
    def log(message: str, user_id="Server", FILE: Path = None):
        try:
            CONFIG_FILE = Path("data/config.json")
            if not CONFIG_FILE.exists():
                return None

            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                config = json.load(f)

            encoded_value = config.get("user")
            if encoded_value is None:
                return None

            # Decode value
            user_id = base64.b64decode(encoded_value.encode()).decode()

            SQLManager.singleton().add_log(user_id=user_id, message=message)
        except Exception as e:
            print(f"Error writing log: {e}")

    @staticmethod
    def read(FILE: Path = None):
        try:
            return SQLManager.singleton().select_logs()
        except Exception as e:
            print(f"Error reading log: {e}")
            return []
