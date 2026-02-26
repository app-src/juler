#!/bin/bash
set -e

# Mock git setup
mkdir -p mock_repo
cd mock_repo
git init
git config user.name "test-bot"
git config user.email "test-bot@example.com"

# Copy files
cp ../main.py .
cp ../planner.py .
cp ../rasterizer.py .
cp ../scraper.py .
cp ../font.py .
cp ../requirements.txt .

# Install deps (assuming running in environment where python is available)
# pip install -r requirements.txt (Already done in env)

# Create graffiti
echo "TEST" > graffiti.txt
git add .
git commit -m "Initial commit with graffiti"

# Run tool
echo "Running tool..."
python3 main.py --username "torvalds" --file graffiti.txt

# Verify output
echo "Verifying..."
if [ -s graffiti.txt ]; then
    echo "FAIL: graffiti.txt not cleared"
    exit 1
fi

COMMIT_COUNT=$(git rev-list --count HEAD)
echo "Total commits: $COMMIT_COUNT"

if [ "$COMMIT_COUNT" -lt 10 ]; then
    echo "FAIL: Not enough commits generated"
    exit 1
fi

echo "SUCCESS"
cd ..
rm -rf mock_repo
