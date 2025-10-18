from datetime import date, datetime, timedelta

import src.database as database
from src.config import (
    DIM_DATE_TABLE_NAME,
    DIM_TITLE_TABLE_NAME,
    FACT_TRANSACTION_TABLE_NAME,
)
from src.decorators import performance_monitor
from src.logger import get_logger
from src.utils import get_all_data, get_all_titles

logger = get_logger("load_in_db")


@performance_monitor
def load_dim_date_table() -> None:
    """
    Populates the date dimension table with all dates for the current year.

    Generates dates from January 1st to December 31st of the current year,
    extracting temporal attributes like year, quarter, month, day, weekday, and week number.
    Only inserts dates that don't already exist in the table to avoid duplicates.
    """
    year = datetime.now().year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        with database.SQLiteDB() as db:
            has_date = db.fetch_one(
                f"SELECT 1 FROM {DIM_DATE_TABLE_NAME} WHERE date = ?", (current_date,)
            )
            if not has_date:
                db.execute_query(
                    f"""
                    INSERT INTO {DIM_DATE_TABLE_NAME} (date, year, quarter, month, day, weekday, week)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        current_date,
                        current_date.year,
                        (current_date.month - 1) // 3 + 1,
                        current_date.month,
                        current_date.day,
                        current_date.weekday(),
                        current_date.isocalendar()[1],
                    ),
                )
                logger.info(f"Date {current_date} added to {DIM_DATE_TABLE_NAME}")
        current_date += timedelta(days=1)


@performance_monitor
def load_title_table() -> None:
    """
    Populates the title dimension table with unique transaction titles.

    Extracts all distinct titles from raw CSV files and inserts them into
    the dimension table, avoiding duplicates by checking for existing titles.
    """
    titles = get_all_titles()
    for title in titles:
        with database.SQLiteDB() as db:
            has_title = db.fetch_one(
                f"SELECT 1 FROM {DIM_TITLE_TABLE_NAME} WHERE title = ?", (title,)
            )
            if not has_title:
                db.execute_query(
                    f"""
                    INSERT INTO {DIM_TITLE_TABLE_NAME} (title)
                    VALUES (?)
                    """,
                    (title,),
                )
                logger.info(f"Title {title} added to {DIM_TITLE_TABLE_NAME}")


@performance_monitor
def load_fact_table() -> None:
    """
    Loads transaction data into the fact table from raw CSV files.

    Processes each transaction record, resolves date and title foreign keys,
    and inserts unique transactions into the fact table while avoiding duplicates.
    Each transaction is linked to its corresponding date and title dimensions.
    """
    data = get_all_data()
    with database.SQLiteDB() as db:
        for item in data:
            date = item["date"]
            title = item["title"]
            amount = item["amount"]
            file_source = item["file_source"]
            date_id = db.fetch_one(
                f"SELECT date_id FROM {DIM_DATE_TABLE_NAME} WHERE date = ?",
                (date,),
            )
            title_id = db.fetch_one(
                f"SELECT title_id FROM {DIM_TITLE_TABLE_NAME} WHERE title = ?",
                (title,),
            )
            has_transaction = db.fetch_one(
                f"SELECT 1 FROM {FACT_TRANSACTION_TABLE_NAME} WHERE date_id = ? AND title_id = ?",
                (date_id[0], title_id[0]),
            )
            if not has_transaction:
                db.execute_query(
                    f"""
                    INSERT INTO {FACT_TRANSACTION_TABLE_NAME} (date_id, title_id, amount, file_source)
                    VALUES (?, ?, ?, ?)
                    """,
                    (date_id[0], title_id[0], amount, file_source),
                )
                logger.info(
                    f"Transaction {date} - {title} - {amount} added to {FACT_TRANSACTION_TABLE_NAME}"
                )


def load_tables() -> None:
    """
    Loads all necessary tables in the database.

    First, it loads the date dimension table with all dates for the current year.
    Then, it loads the title dimension table with all unique transaction titles.
    Finally, it loads the fact table with transaction data from raw CSV files.

    This function is a convenience wrapper for the individual loading functions.
    """
    load_dim_date_table()
    load_title_table()
    load_fact_table()


if __name__ == "__main__":
    pass
