#!/bin/bash
set -e

# Setup directories
rm -rf simulation
mkdir -p simulation/tool_repo
mkdir -p simulation/target_repo

# Setup target repo (where pixels go)
cd simulation/target_repo
git init
git config user.name "target-bot"
git config user.email "target-bot@example.com"
git commit --allow-empty -m "Initial target commit"
TARGET_REPO_PATH=$(pwd)
cd ../..

# Setup tool repo (where script and input file live)
cd simulation/tool_repo
git init
git config user.name "tool-bot"
git config user.email "tool-bot@example.com"

# Copy files
cp ../../main.py .
cp ../../planner.py .
cp ../../rasterizer.py .
cp ../../scraper.py .
cp ../../font.py .
cp ../../requirements.txt .

# Create graffiti
echo "DUAL" > graffiti.txt
git add .
git commit -m "Initial tool commit"

# Run tool pointing to target repo
echo "Running tool with --repo $TARGET_REPO_PATH"
python3 main.py --username "torvalds" --file graffiti.txt --repo "$TARGET_REPO_PATH"

# Verify Tool Repo (Cleanup)
echo "Verifying Tool Repo..."
if [ -s graffiti.txt ]; then
    echo "FAIL: graffiti.txt not cleared in tool repo"
    exit 1
fi
TOOL_COMMITS=$(git rev-list --count HEAD)
# Initial + Cleanup = 2
if [ "$TOOL_COMMITS" -ne 2 ]; then
     echo "FAIL: Tool repo commit count unexpected: $TOOL_COMMITS"
     exit 1
fi

# Verify Target Repo (Pixels)
echo "Verifying Target Repo..."
cd "$TARGET_REPO_PATH"
TARGET_COMMITS=$(git rev-list --count HEAD)
echo "Target repo total commits: $TARGET_COMMITS"

if [ "$TARGET_COMMITS" -lt 10 ]; then
    echo "FAIL: Target repo has too few commits"
    exit 1
fi

echo "SUCCESS: Dual repo simulation passed."
cd ../..
rm -rf simulation
