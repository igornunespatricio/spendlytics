.PHONY: format lint check quality

# Directories to check
CODE_DIRS = src app

# Main command - use this for development
quality:
	ruff check --fix --output-format=concise $(CODE_DIRS)
	black $(CODE_DIRS)

# Check only (for CI/pre-commit)
check:
	ruff check --output-format=concise $(CODE_DIRS)
	black --check $(CODE_DIRS)

# Individual commands if needed
format:
	black $(CODE_DIRS)

lint:
	ruff check --output-format=concise $(CODE_DIRS)

fix:
	ruff check --fix --output-format=concise $(CODE_DIRS)

# CI command (strict with GitHub format)
ci:
	ruff check --output-format=github $(CODE_DIRS)
	black --check --diff $(CODE_DIRS)