import sqlite3


class Database:
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(f"{db_name}.db", check_same_thread=False)

    def check_if_table_exists(self, table_name: str) -> bool:
        """Return True if table with specified name exists, else False.

        Args:
            table_name (str): name of table

        Returns:
            bool: True if table exists in database, else False
        """
        return self.get_cursor().execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name=(?)",
            (table_name,)
        ).fetchone()[0] == 1

    def get_cursor(self):
        return self.con.cursor()

    def commit_db(self):
        self.con.commit()
