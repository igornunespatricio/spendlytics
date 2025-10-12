import sqlite3
import os
from pathlib import Path

RAW_PATH = r"data\raw"

def read_raw():
    # iterate files in raw folder
    files = Path(RAW_PATH).glob("*.txt")
    for file in files:
        print(file)
        

if __name__ == "__main__":
    read_raw()