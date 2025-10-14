RAW_DATA_PATH = r"data/raw"
DB_PATH = r"data/transactions.db"
LOGGER_PATH = r"logs"
DIM_DATE_TABLE_NAME = "dim_date"
DIM_TITLE_TABLE_NAME = "dim_title"
FACT_TRANSACTION_TABLE_NAME = "fact_transactions"

DIM_DATE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {DIM_DATE_TABLE_NAME} (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    weekday INTEGER,
    week INTEGER
);
"""

DIM_TITLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {DIM_TITLE_TABLE_NAME} (
    title_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE
);
"""

FACT_TRANSACTION_QUERY = f"""
CREATE TABLE IF NOT EXISTS {FACT_TRANSACTION_TABLE_NAME} (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER NOT NULL,
    title_id INTEGER NOT NULL,
    file_source TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (title_id) REFERENCES dim_title(title_id)
);
"""

INDEX_QUERIES = """
CREATE INDEX IF NOT EXISTS idx_fact_file_source ON fact_transactions(file_source);
"""
