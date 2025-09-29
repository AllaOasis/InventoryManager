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
#  - mysql-connect for database integration

import json
import base64
import sqlite3
import mysql.connector
from pathlib import Path

class SQLManager:
    SELF = None  # This is the class-level singleton reference

    @staticmethod
    def singleton():
        """Static method to return the singleton instance."""
        if SQLManager.SELF is None:  # Check if the singleton has been created
            SQLManager.SELF = SQLManager()  # Create it if it doesn't exist
            SQLManager.singleton().config_connect() # Auto-Connect feature
        return SQLManager.SELF  # Return the singleton instance

    def __init__(self, HOST="", USER="", PASSWORD="", DATABASE="", PORT=3306):
        self.connect(HOST, USER, PASSWORD, DATABASE, PORT)

    def connect(self, HOST="", USER="", PASSWORD="", DATABASE="", PORT=3306):
        try:
            # Attempt MySQL connection
            self.conn = mysql.connector.connect(
                host=HOST,
                port=PORT,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            self.cur = self.conn.cursor()
            # Create Tables if they don't exist (MySQL)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    code VARCHAR(255) UNIQUE NOT NULL,
                    qty INT NOT NULL
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id VARCHAR(255) NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message VARCHAR(255) NOT NULL
                )
            """)
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"MySQL connection failed: {e}, falling back to SQLite")
            FILE = Path("data/inventory.db")

            # Ensure the parent folder exists
            FILE.parent.mkdir(parents=True, exist_ok=True)

            self.conn = sqlite3.connect(FILE)
            self.cur = self.conn.cursor()
            # Create Tables if they don't exist (SQLite)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    qty INTEGER NOT NULL
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message TEXT NOT NULL
                )
            """)
            self.conn.commit()
        
    def config_connect(self):
        self.connect(
            SQLManager.load_config("host"),
            SQLManager.load_config("user"),
            SQLManager.load_config("password"),
            SQLManager.load_config("database"),
            SQLManager.load_config("port")
        )

    @staticmethod
    def connection_test(HOST, USER, PASSWORD, DATABASE, PORT=3306):
        try:
            # Attempt MySQL connection
            conn = mysql.connector.connect(
                host=HOST,
                port=PORT,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
                
            if conn.is_connected():
                conn.close()
                return True
            return False
        except Exception as e:
            print(f"Error executing query: {e}")
            return False

    def execute_query(self, query, params=None):
        """Execute a query (insert, update, delete, or select) on the database."""
        try:
            self.cur.execute(query, params or ())
            
            # Commit **only for write queries**
            if query.strip().lower().startswith(('insert', 'update', 'delete')):
                self.conn.commit()
            
            # Return results for SELECT queries
            if query.strip().lower().startswith('select'):
                return self.cur.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()


    # ---------------
    # Items
    # ---------------

    def add_item(self, name, code, quantity):
        """Add an item to the inventory."""
        query = (
            "INSERT INTO inventory (name, code, qty) VALUES (%s, %s, %s)"
            if isinstance(self.conn, mysql.connector.MySQLConnection)
            else "INSERT INTO inventory (name, code, qty) VALUES (?, ?, ?)"
        )
        self.execute_query(query, (name, code, quantity))

    def remove_item(self, item_id):
        """Remove an item from the inventory by ID."""
        query = (
            "DELETE FROM inventory WHERE id = %s"
            if isinstance(self.conn, mysql.connector.MySQLConnection)
            else "DELETE FROM inventory WHERE id = ?"
        )
        self.execute_query(query, (item_id,))

    def update_item(self, item_id, name, code, quantity):
        """Update an item in the inventory by ID."""
        query = (
            "UPDATE inventory SET name = %s, code = %s, qty = %s WHERE id = %s"
            if isinstance(self.conn, mysql.connector.MySQLConnection)
            else "UPDATE inventory SET name = ?, code = ?, qty = ? WHERE id = ?"
        )
        self.execute_query(query, (name, code, quantity, item_id))

    def select_items(self):
        """Select all items from the inventory."""
        query = "SELECT * FROM inventory"
        return self.execute_query(query)
    
    # ---------------
    # Logs
    # ---------------

    def add_log(self, user_id, message):
        """Add a log entry."""
        query = (
            "INSERT INTO logs (user_id, message) VALUES (%s, %s)"
            if isinstance(self.conn, mysql.connector.MySQLConnection)
            else "INSERT INTO logs (user_id, message) VALUES (?, ?)"
        )
        self.execute_query(query, (user_id, message))

    def select_logs(self):
        """Select all logs."""
        query = "SELECT * FROM logs"
        return self.execute_query(query)


    
    @staticmethod
    def save_config(parameter: str, value):
        CONFIG_FILE = Path("data/config.json")
        CONFIG_FILE.parent.mkdir(exist_ok=True)  # make sure 'data/' exists

        config = {}  # initialize in case file doesn't exist
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                config = json.load(f)

        # Add or update the parameter
        encoded_value = base64.b64encode(value.encode()).decode()
        config[parameter] = encoded_value

        # Save back to file
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)  # pretty formatting

    @staticmethod
    def load_config(parameter: str) -> str:
        CONFIG_FILE = Path("data/config.json")
        if not CONFIG_FILE.exists():
            return None

        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            config = json.load(f)

        encoded_value = config.get(parameter)
        if encoded_value is None:
            return None

        # Decode value
        return base64.b64decode(encoded_value.encode()).decode()


# Example usage
#if __name__ == "__main__":
#    # Example for creating a connection
#    sql_manager = SQLManager()
#    
#    # Add a new item
#    sql_manager.add_item("Widget", "W123", 10)
#    
#    # Update an item (assuming item with id 1 exists)
#    sql_manager.update_item(1, "Widget Pro", "W124", 15)
#    
#    # Select and display all items
#    items = sql_manager.select_items()
#    print(items)
#    
#    # Remove an item (assuming item with id 1 exists)
#    sql_manager.remove_item(1)
