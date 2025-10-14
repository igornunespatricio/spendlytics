from datetime import datetime, date, timedelta
import src.database as database
from src.logger import get_logger
from src.config import (
    DIM_DATE_TABLE_NAME,
    DIM_TITLE_TABLE_NAME,
    FACT_TRANSACTION_TABLE_NAME,
)
from src.utils import get_all_titles, get_all_data

logger = get_logger("load_in_db")


def load_dim_date_table() -> None:
    """add dates to date table"""
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


def load_title_table() -> None:
    """add titles to title table"""
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
                logger.info((f"Title {title} added to {DIM_TITLE_TABLE_NAME}"))


# TODO: implement this function
def load_fact_table() -> None:
    """add transactions to fact table"""
    data = get_all_data()
    with database.SQLiteDB() as db:
        for i, item in enumerate(data):
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
                    (
                        f"Transaction {date} - {title} - {amount} added to {FACT_TRANSACTION_TABLE_NAME}"
                    )
                )


def load_tables() -> None:
    load_dim_date_table()
    load_title_table()
    load_fact_table()


if __name__ == "__main__":
    pass
