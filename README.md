# GitHub Graffiti Tool

This tool allows you to "write" text on your GitHub contribution graph by automatically generating commits with backdated timestamps.

## Features

- **Pixel Art**: Converts text into a 5x7 bitmap font displayed across the last year of your contribution graph.
- **Adaptive Intensity**: Fetches your profile stats to generate commit counts relative to your average activity (2x intensity), making the text stand out.
- **Automatic Cleanup**: After processing, the input file is cleared, so you don't accidentally re-run the same graffiti.
- **CI/CD Integration**: Includes a GitHub Action workflow to run automatically or on demand.

## Setup

1.  **Use this Template/Repo**: Fork or create a repository from this code.
2.  **Enable Actions**: Ensure GitHub Actions are enabled in your repository settings.
3.  **Permissions**: Ensure the default `GITHUB_TOKEN` has `contents: write` permissions (usually default for private repos, but check Settings > Actions > General > Workflow permissions).

## Usage

1.  Create a file named `graffiti.txt` in the root of your repository.
2.  Write the text you want to appear on your graph (e.g., "HELLO").
    *   *Note: The grid is 52 columns wide. Short text (3-6 chars) works best.*
3.  Commit and push the `graffiti.txt` file.
4.  **Wait** for the scheduled workflow (midnight UTC) OR manually trigger it:
    *   Go to **Actions** tab.
    *   Select **Graffiti Contribution Graph**.
    *   Click **Run workflow**.

The action will:
1.  Read `graffiti.txt`.
2.  Calculate the commit plan.
3.  Generate backdated empty commits.
4.  Clear `graffiti.txt`.
5.  Push the changes back to your repository.

## Configuration

The script uses environment variables or CLI arguments:

- `--username`: The GitHub username to fetch stats for (defaults to repo owner in CI).
- `--file`: The input file path (default: `graffiti.txt`).
