import src.database as database
from src.config import (
    DIM_DATE_TABLE_NAME,
    DIM_TITLE_TABLE_NAME,
    FACT_TRANSACTION_TABLE_NAME,
)
from src.logger import get_logger

logger = get_logger("calculate_metrics")


def calculate_amount_spent_per_month() -> None:
    """
    Calculates and stores monthly spending totals in a summary table.

    Creates a monthly_spending_summary table aggregating transaction amounts
    by year and month, excluding income transactions (titles containing 'Pagamento recebido').
    The summary provides quick access to monthly spending trends without complex queries.
    """
    with database.SQLiteDB() as db:
        # Create the summary table
        db.execute_query(
            """CREATE TABLE IF NOT EXISTS monthly_spending_summary (
                year INTEGER,
                month INTEGER,
                total_amount REAL,
                PRIMARY KEY (year, month)
            )"""
        )

        # Clear existing data (optional)
        db.execute_query("DELETE FROM monthly_spending_summary")

        # Fetch the data
        data = db.fetch_all(
            f"""SELECT d.year, d.month, SUM(f.amount) FROM {FACT_TRANSACTION_TABLE_NAME} as f
            LEFT JOIN {DIM_DATE_TABLE_NAME} AS d ON f.date_id = d.date_id
            LEFT JOIN {DIM_TITLE_TABLE_NAME} AS t ON f.title_id = t.title_id
            WHERE t.title <> 'Pagamento recebido'
            GROUP BY d.year, d.month"""
        )

        # Insert each row
        for year, month, amount in data:
            db.execute_query(
                "INSERT INTO monthly_spending_summary (year, month, total_amount) VALUES (?, ?, ?)",
                (year, month, amount),
            )
        logger.info("Monthly spending summary updated")


def calculate_amount_spent_per_title() -> None:
    """
    Calculates and stores spending totals per transaction title in a summary table.

    Creates a title_spending_summary table aggregating transaction amounts
    by title, excluding income transactions (titles containing 'Pagamento recebido').
    Provides quick insights into spending patterns by category or merchant.
    """
    with database.SQLiteDB() as db:
        # Create the summary table
        db.execute_query(
            """CREATE TABLE IF NOT EXISTS title_spending_summary (
                title_id INTEGER,
                title TEXT,
                total_amount REAL,
                PRIMARY KEY (title_id)
            )"""
        )

        # Clear existing data (optional)
        db.execute_query("DELETE FROM title_spending_summary")

        # Fetch the data
        data = db.fetch_all(
            f"""SELECT t.title_id, t.title, SUM(f.amount)
            FROM {FACT_TRANSACTION_TABLE_NAME} as f
            LEFT JOIN {DIM_TITLE_TABLE_NAME} AS t ON f.title_id = t.title_id
            WHERE t.title <> 'Pagamento recebido'
            GROUP BY t.title_id, t.title"""
        )

        # Insert each row
        for title_id, title, amount in data:
            db.execute_query(
                "INSERT INTO title_spending_summary (title_id, title, total_amount) VALUES (?, ?, ?)",
                (title_id, title, amount),
            )
        logger.info("Title spending summary updated")


def calculate_metrics():
    calculate_amount_spent_per_month()
    calculate_amount_spent_per_title()


if __name__ == "__main__":
    calculate_metrics()
