import os
import subprocess
import argparse
import sys
from datetime import datetime
from rasterizer import rasterize_text, print_grid
from scraper import fetch_user_stats
from planner import plan_commits

def execute_plan(plan):
    """
    Executes the commit plan using git commands.
    """
    total = sum(count for _, count in plan)
    print(f"Executing plan: {len(plan)} days, {total} total commits.")

    current = 0
    # Use environment for committer date
    env = os.environ.copy()

    for date_str, count_needed in plan:
        # We need to set GIT_AUTHOR_DATE and GIT_COMMITTER_DATE
        full_date = f"{date_str} 12:00:00"

        env["GIT_AUTHOR_DATE"] = full_date
        env["GIT_COMMITTER_DATE"] = full_date

        for i in range(count_needed):
            cmd = [
                "git", "commit", "--allow-empty",
                "-m", "Graffiti pixel"
            ]

            try:
                subprocess.run(cmd, env=env, check=True, stdout=subprocess.DEVNULL)
                current += 1
                if current % 10 == 0:
                    print(f"Progress: {current}/{total}...", end='\r')
            except subprocess.CalledProcessError as e:
                print(f"Error creating commit: {e}")

    print(f"\nDone. {current} commits created.")

def process_input_file(filepath, username):
    if not os.path.exists(filepath):
        print(f"Input file {filepath} not found.")
        return

    with open(filepath, 'r') as f:
        text = f.read().strip()

    if not text:
        print("Input file is empty. Nothing to do.")
        return

    print(f"Processing text: '{text}' for user: {username}")

    # 1. Rasterize
    grid = rasterize_text(text)
    print("Rasterized Grid:")
    print_grid(grid)

    # 2. Fetch Stats
    print("Fetching user stats...")
    stats = fetch_user_stats(username)
    if not stats or stats[1] == 0:
        print("Could not fetch stats or user has no activity. Using defaults.")
        # Default fallback
        stats = ({}, 5.0)
    else:
        print(f"Found {len(stats[0])} days of history. Average activity: {stats[1]:.2f}")

    # 3. Plan
    print("Planning commits...")
    plan = plan_commits(grid, stats, intensity_multiplier=2)

    if not plan:
        print("No commits needed (maybe grid is empty or target already reached).")
    else:
        # 4. Execute
        execute_plan(plan)

    # 5. Cleanup
    print("Cleaning up input file...")
    with open(filepath, 'w') as f:
        f.write("")

    # Commit the cleanup with CURRENT time
    try:
        subprocess.run(["git", "add", filepath], check=True)
        # Use default env (current time) for this commit
        subprocess.run(["git", "commit", "-m", "Clear graffiti queue"], check=True)
        print("Cleanup committed.")
    except subprocess.CalledProcessError as e:
        print(f"Error committing cleanup: {e}")

def main():
    parser = argparse.ArgumentParser(description='GitHub Graffiti Tool')
    parser.add_argument('--username', type=str, required=True, help='GitHub username')
    parser.add_argument('--file', type=str, default=os.environ.get('GRAFFITI_INPUT_FILE', 'graffiti.txt'), help='Input file path')

    args = parser.parse_args()

    process_input_file(args.file, args.username)

if __name__ == "__main__":
    main()
