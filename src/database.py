import sqlite3
from datetime import datetime
from typing import Any

from src.config import DB_PATH, FACT_METRICS_TABLE_NAME


class SQLiteDB:
    """
    A context manager for SQLite database operations.

    Provides a simple interface for executing queries, fetching data,
    and managing database connections with automatic commit and cleanup.

    Attributes:
        db_path (str): Path to the SQLite database file
        connection (sqlite3.Connection): Active database connection
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.connection: sqlite3.Connection | None = None

    def __enter__(self):
        """Establishes database connection when entering context."""
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits transactions and closes connection when exiting context."""
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def execute_query(self, query: str, params: tuple[Any, ...] = ()) -> None:
        """Executes a SQL query that doesn't return data (INSERT, UPDATE, DELETE)."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[tuple[Any]]:
        """Executes a SQL query and returns all results."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> tuple[Any] | None:
        """Executes a SQL query and returns the first result, or None if no results."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()


def log_function_metrics(
    function_name: str,
    execution_time: float,
    status: str,
    error_message: str | None = None,
) -> None:
    """
    Logs function performance metrics to the database.

    Records function execution details including name, duration, timestamp,
    completion status, and optional error message for performance monitoring.

    Args:
        function_name (str): Name of the executed function
        execution_time (float): Duration of execution in seconds
        status (str): Execution status ("completed" or "failed")
        error_message (str | None): Error message if function failed, None otherwise
    """
    with SQLiteDB() as db:
        db.execute_query(
            f"""
            INSERT INTO {FACT_METRICS_TABLE_NAME}
            (function_name, execution_time, timestamp, status, error_message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (function_name, execution_time, datetime.now(), status, error_message),
        )
