from src.load_in_db import load_tables
from src.utils import create_database


def main() -> None:
    create_database()
    load_tables()


if __name__ == "__main__":
    main()
