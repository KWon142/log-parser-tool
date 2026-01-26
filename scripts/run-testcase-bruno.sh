#!/bin/bash
#folder 'scripts')
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# SCRIPT_DIR/..  navigate to bru collection
COLLECTION_PATH="$(cd "$SCRIPT_DIR/../tests/learning-bruno/api-verification" && pwd)"
# Run collection's testcases
echo "🚀 Running Bruno Collection from: $COLLECTION_PATH"
cd "$COLLECTION_PATH"
bru run  --reporter-json results.json --reporter-html results.html 
