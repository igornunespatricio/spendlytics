#!/bin/bash

# Script to automatically generate project documentation
set -e

PROJECT_NAME="Spendlytics"
PROJECT_DESCRIPTION="A financial analytics application for tracking and analyzing spending patterns."

# Create/update the main README.md with structure embedded
cat > README.md << EOF
# $PROJECT_NAME

$PROJECT_DESCRIPTION

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry (dependency management)

### Installation
\`\`\`bash
# Clone the repository
git clone <your-repo-url>
cd $PROJECT_NAME

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
\`\`\`

### Running the Application
\`\`\`bash
poetry run python main.py
\`\`\`

### Development
\`\`\`bash
# Code quality checks
make quality    # Auto-fix and format
make check      # Verify code quality

# Individual tools
make format     # Format code with Black
make lint       # Lint with Ruff
\`\`\`

## Project Structure

\`\`\`
$(tree -I '.git|__pycache__|.venv')
\`\`\`

## Code Quality

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **Pre-commit** hooks for automated quality checks

Run \`make quality\` before committing to ensure code standards.
EOF

echo "✅ README.md updated successfully with project structure!"