#!/bin/bash

# Exit immediately if a command fails
set -e

# Resolve the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=========================================="
echo "🚀 Launching Unit Tests with Pytest..."
echo "📂 Project Root: $PROJECT_ROOT"
echo "=========================================="

# Navigate to project root
cd "$PROJECT_ROOT"

# Run pytest via uv, passing all CLI arguments
uv run pytest tests/ "$@"

echo "=========================================="
echo "✅ Testing completed!"
echo "=========================================="