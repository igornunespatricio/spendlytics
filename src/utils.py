import csv
from pathlib import Path

import src.database as database
from src.config import (
    DIM_DATE_QUERY,
    DIM_TITLE_QUERY,
    FACT_METRICS_TABLE_QUERY,
    FACT_TRANSACTION_QUERY,
    INDEX_QUERIES,
    RAW_DATA_PATH,
)
from src.decorators import performance_monitor


@performance_monitor
def create_database():
    """
    Initializes the database by creating all necessary tables and indexes.

    This function creates the following database schema:
    - Dimension tables (date, title) for data categorization
    - Fact tables (transactions, function_metrics) for core data and monitoring
    - Indexes for optimized query performance

    Tables Created:
    - dim_date: Date dimension for time-based analysis
    - dim_title: Title dimension for transaction categorization
    - fact_transaction: Main transaction facts with amounts and relationships
    - function_metrics: Performance monitoring data for function execution

    The function uses predefined SQL queries from config to ensure consistent
    schema creation across environments.

    Raises:
        DatabaseError: If any table creation query fails
        OperationalError: If database file cannot be accessed or created
    """
    # create the tables
    with database.SQLiteDB() as db:
        db.execute_query(DIM_DATE_QUERY)
        db.execute_query(DIM_TITLE_QUERY)
        db.execute_query(FACT_TRANSACTION_QUERY)
        db.execute_query(FACT_METRICS_TABLE_QUERY)
        db.execute_query(INDEX_QUERIES)


def get_raw_csv_files() -> list[Path]:
    """Returns a list of all CSV file paths in the raw data directory."""
    files = list(Path(RAW_DATA_PATH).glob("*.csv"))
    return files


def get_all_titles() -> list[str]:
    """Extracts all unique transaction titles from raw CSV files."""
    titles = []
    files = get_raw_csv_files()
    for file in files:
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                titles.append(row["title"])
    return titles


def get_all_data() -> list[str]:
    """Reads and combines all transaction data from raw CSV files."""
    data = []
    files = get_raw_csv_files()
    for file in files:
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["file_source"] = file.name
                data.append(row)
    return data


if __name__ == "__main__":
    # create_database()
    # get_all_titles()
    for i, item in enumerate(get_all_data()):
        print(item)
        if i == 2:
            exit()
    pass
