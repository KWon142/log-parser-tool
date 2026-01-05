#!/bin/bash

# Exit immediately if a command fails
set -e

# Resolve the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PROJECT_BASH="$(cd "$PROJECT_ROOT/tests/learning-fastAPI" && pwd)"
echo "=========================================="
echo "🚀 Launching Unit Tests with Pytest..."
echo "📂 Project Root: $PROJECT_BASH"
echo "=========================================="

# Navigate to project bash
cd "$PROJECT_BASH"

echo "=========================================="
echo "✅ Starting Bookstore Server Completed!!! "
echo "=========================================="

# Run Bookstore Server in learning-fastAPI
uv run fastapi dev bookstore_db.py

