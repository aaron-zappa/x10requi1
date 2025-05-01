# python requi_db_handler.py
# supports e.g. handling, creation, filling of the requi.db data
import sqlite3
import sys
import argparse
import os


class RequiDBHandler():
    def __init__(self, db_file="requi.db"):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """Connect to the SQLite database or create it if it doesn't exist."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Connected to database: {self.db_file}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        """Disconnect from the SQLite database."""
        if self.conn:
            self.conn.close()
            print("Disconnected from database.")

    def drop_system_param_table(self):
        """Drops the SystemParam table."""
        if not self.conn:
            print("Not connected to database.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS SystemParam")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error dropping SystemParam table: {e}")

    def create_system_param_table(self):
        """Create the SystemParam table."""

        try:
            cursor = self.conn.cursor()
            # Drop the table if it exists
            cursor.execute("DROP TABLE IF EXISTS SystemParam")
            cursor.execute(
                """
                CREATE TABLE SystemParam (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    param_cat TEXT,
                    param_code TEXT,
                    descrip TEXT
                )
            """
            )
            # Create an index on param_cat and param_code for faster lookups
            cursor.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_system_param_unique ON SystemParam (param_cat, param_code);
                """
            )

            self.conn.commit()
            print("SystemParam table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating SystemParam table: {e}")

    def fill_system_param_table(self):
        """Fill the SystemParam table with predefined data based on new structure."""

        system_params = [
            {"phase": "initial_collect", "description": "Initial Collection Phase"},
            {"phase": "first_refine", "description": "First Refinement Phase"},            
            {"timeline": "short", "description": "Short-Term"},
            {"timeline": "mid", "description": "Mid-Term"},
            {"timeline": "long term", "description": "Long-Term"},
        ]

        try:
            cursor = self.conn.cursor()
            for param in system_params:
                param_cat = list(param.keys())[0]  # Get 'phase' or 'timeline'
                param_code = param[param_cat]
                descrip = param["description"]
                cursor.execute(
                    "INSERT OR IGNORE INTO SystemParam (param_cat, param_code, descrip) VALUES (?, ?, ?)",
                    (param_cat, param_code, descrip)
                )
            self.conn.commit()
            print("SystemParam table filled successfully.")
        except sqlite3.Error as e:
            print(f"Error filling systemparam table: {e}")


def confirm_action():
    """Asks the user for confirmation."""
    while True:
        response = input("Are you sure you want to proceed? (yes/no): ").lower()
        if response in ["yes", "no"]:
            return response == "yes"
        print("Please enter 'yes' or 'no'.")


def ensure_csv_folder():
    """Ensures that the csv folder exists."""
    if not os.path.exists("csv"):
        os.makedirs("csv")
        print("Created 'csv' folder.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RequiDBHandler - Database management tool.")
    parser.add_argument("action", choices=["fill_system_params", "create_initial_db"],
                        help="Action to perform: fill_system_params or create_initial_db")

    args = parser.parse_args()

    db_handler = None
    try:
        db_handler = RequiDBHandler()
        db_handler.connect()
        if args.action == "fill_system_params":
            db_handler.fill_system_param_table()

        elif args.action == "create_initial_db":
            #check user confimation
            if confirm_action():
                db_handler.drop_system_param_table()
                db_handler.create_system_param_table()

                # ensure that csv folder is there
                ensure_csv_folder()
            else:
                print("Action cancelled by user.")

        else:
            print("Invalid argument for action.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if db_handler:
            db_handler.disconnect()















