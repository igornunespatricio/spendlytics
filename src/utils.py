import src.database as database
from pathlib import Path
import csv
from src.config import (
    RAW_DATA_PATH,
    DB_PATH,
    DIM_DATE_QUERY,
    DIM_TITLE_QUERY,
    FACT_TRANSACTION_QUERY,
    INDEX_QUERIES,
)


def create_database():
    """Creates the database file and the tables"""
    # create the tables
    with database.SQLiteDB() as db:
        db.execute_query(DIM_DATE_QUERY)
        db.execute_query(DIM_TITLE_QUERY)
        db.execute_query(FACT_TRANSACTION_QUERY)
        db.execute_query(INDEX_QUERIES)


def get_raw_csv_files() -> list[Path]:
    """return list of csv filepaths in the RAW_DATA_PATH directory"""
    files = list(Path(RAW_DATA_PATH).glob("*.csv"))
    return files


def get_all_titles() -> list[str]:
    """get all distinct titles from raw files"""
    titles = []
    files = get_raw_csv_files()
    for file in files:
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                titles.append(row["title"])
    return titles


def get_all_data() -> list[str]:
    """get all data from raw files"""
    data = []
    files = get_raw_csv_files()
    for file in files:
        with open(file, "r") as f:
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
