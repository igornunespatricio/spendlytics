# Spendlytics

A financial analytics application for tracking and analyzing spending patterns.

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry (dependency management)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd Spendlytics

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running the Application
```bash
poetry run python main.py
```

### Development
```bash
# Code quality checks
make quality    # Auto-fix and format
make check      # Verify code quality

# Individual tools
make format     # Format code with Black
make lint       # Lint with Ruff
```

## Project Structure

```
.
├── LICENSE
├── Makefile
├── README.md
├── STRUCTURE.md
├── app
│   ├── Home.py
│   ├── __init__.py
│   └── pages
│       ├── Detailed.py
│       ├── Summary.py
│       └── __init__.py
├── data
│   ├── raw
│   │   ├── Nubank_2025-09-08.csv
│   │   ├── Nubank_2025-10-08.csv
│   │   └── Nubank_2025-11-08.csv
│   └── transactions.db
├── logs
│   └── load_in_db.log
├── main.py
├── poetry.lock
├── pyproject.toml
├── scripts
│   ├── create_readme.sh
│   └── create_structure.sh
└── src
    ├── __init__.py
    ├── calculate_metrics.py
    ├── config.py
    ├── database.py
    ├── load_in_db.py
    ├── logger.py
    └── utils.py

8 directories, 26 files
```

## Code Quality

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **Pre-commit** hooks for automated quality checks

Run `make quality` before committing to ensure code standards.
