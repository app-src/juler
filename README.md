# GitHub Graffiti Tool

This tool allows you to "write" text on your GitHub contribution graph by automatically generating commits with backdated timestamps.

## Features

- **Pixel Art**: Converts text into a 5x7 bitmap font displayed across the last year of your contribution graph.
- **Adaptive Intensity**: Fetches your profile stats to generate commit counts relative to your average activity (2x intensity), making the text stand out.
- **Dual Repository Support**: Can generate commits in a separate "canvas" repository to keep your main tool repository clean.
- **Automatic Cleanup**: After processing, the input file is cleared, so you don't accidentally re-run the same graffiti.
- **CI/CD Integration**: Includes a GitHub Action workflow to run automatically or on demand.

## Setup

1.  **Use this Template/Repo**: Fork or create a repository from this code (the "Tool Repo").
2.  **Enable Actions**: Ensure GitHub Actions are enabled in your repository settings.
3.  **Permissions**: Ensure the default `GITHUB_TOKEN` has `contents: write` permissions.

### Option A: Commit to This Repo (Simplest)
By default, the tool will generate commits in the same repository where it runs.

### Option B: Commit to a Separate Repo (Cleaner)
To keep your history clean, you can target a separate repository (e.g., `username/graffiti-canvas`).

1.  Create a new empty repository (the "Target Repo").
2.  Create a **Personal Access Token (PAT)** with `repo` scope (or `contents: write` if fine-grained).
3.  In your Tool Repo, go to **Settings > Secrets and variables > Actions**.
4.  Add a repository secret:
    *   Name: `TARGET_REPO_TOKEN`
    *   Value: (Your PAT)
5.  (Optional) Add a repository secret for the default target repo name:
    *   Name: `TARGET_REPO_NAME`
    *   Value: `username/graffiti-canvas`

## Usage

1.  Create or edit `graffiti.txt` in the root of your Tool Repo.
2.  Write the text you want to appear on your graph (e.g., "HELLO").
    *   *Note: The grid is 52 columns wide. Short text (3-6 chars) works best.*
3.  Commit and push the `graffiti.txt` file.
4.  **Wait** for the scheduled workflow (midnight UTC) OR manually trigger it:
    *   Go to **Actions** tab.
    *   Select **Graffiti Contribution Graph**.
    *   Click **Run workflow**.
    *   (If using Option B) Enter the target repository name if prompted/not set as secret.

The action will:
1.  Read `graffiti.txt`.
2.  Calculate the commit plan.
3.  Checkout the Target Repo and generate backdated empty commits there.
4.  Push the Target Repo updates.
5.  Clear `graffiti.txt` in the Tool Repo.
6.  Push the Tool Repo updates.

## Configuration

The script uses environment variables or CLI arguments:

- `--username`: The GitHub username to fetch stats for (defaults to repo owner in CI).
- `--file`: The input file path (default: `graffiti.txt`).
- `--repo`: The path to the repository where pixel commits should be created.
