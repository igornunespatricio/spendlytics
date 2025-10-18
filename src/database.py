import sqlite3
from typing import Any

from src.config import DB_PATH


class SQLiteDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.connection: sqlite3.Connection | None = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def execute_query(self, query: str, params: tuple[Any, ...] = ()) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[tuple[Any]]:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> tuple[Any] | None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
