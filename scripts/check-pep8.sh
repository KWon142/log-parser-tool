#!/bin/bash

# Exit immediately if any command returns a non-zero status
set -e

# Determine the project root directory
# This resolves the directory where the script is located, then moves one level up
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=========================================="
echo "🕵️  Checking PEP-8 Compliance..."
echo "=========================================="

# Change working directory to the project root
cd "$PROJECT_ROOT"

# --------------------------------------------------
# 1. Check for logic errors and coding style issues
#    (Equivalent to Flake8)
#
# --select E,W,F,N:
# E, W : Standard PEP 8 errors and warnings
# F    : Pyflakes (detects logical errors)
# N    : PEP 8 Naming (enforces snake_case, etc.)
# --------------------------------------------------
uv run ruff check . --select E,W,F,N

# --------------------------------------------------
# 2. Check code formatting
#    (Whitespace, line breaks – equivalent to Black)
#
# --check: Report formatting issues with applying auto-fixing with refix --fix
# --------------------------------------------------
if [[ "$@" == *"--fix"* ]]; then
    echo "✨ Applying auto-formatting..."
    uv run ruff format .
else
    # Mặc định chỉ check xem format có đúng không
    uv run ruff format --check .
fi


echo "=========================================="
echo "✅  Excellent! Code conforms to PEP-8."
echo "=========================================="
