RAW_DATA_PATH = r"data/raw"
DB_PATH = r"data/transactions.db"
LOGGER_PATH = r"logs"
DIM_DATE_TABLE_NAME = "dim_date"
DIM_TITLE_TABLE_NAME = "dim_title"
FACT_TRANSACTION_TABLE_NAME = "fact_transactions"
FACT_METRICS_TABLE_NAME = "function_metrics"

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

INDEX_QUERIES = f"""
CREATE INDEX IF NOT EXISTS idx_fact_file_source ON {FACT_TRANSACTION_TABLE_NAME}(file_source);
"""

# Add this to your existing config.py
FACT_METRICS_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {FACT_METRICS_TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    function_name TEXT NOT NULL,
    execution_time REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    error_message TEXT
);
"""
