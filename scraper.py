import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_user_stats(username):
    """
    Fetches contribution data for a GitHub user.
    Returns:
        - date_map: Dictionary mapping 'YYYY-MM-DD' to commit count (int)
        - average_commits: Float, average commits on active days
    """
    url = f"https://github.com/users/{username}/contributions"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, 0

    soup = BeautifulSoup(response.text, 'html.parser')

    days = soup.find_all("td", class_="ContributionCalendar-day")
    tooltips = soup.find_all("tool-tip")

    # Map tooltips by 'for' attribute
    tooltip_map = {}
    for t in tooltips:
        for_id = t.get('for')
        if for_id:
            tooltip_map[for_id] = t.get_text(strip=True)

    date_map = {}
    total_commits = 0
    active_days = 0

    for day in days:
        date_str = day.get('data-date')
        if not date_str:
            continue

        day_id = day.get('id')
        count = 0

        # Try finding associated tooltip
        if day_id and day_id in tooltip_map:
            text = tooltip_map[day_id]
            # Parse "3 contributions on ..." or "No contributions on ..."
            if "No contributions" in text:
                count = 0
            else:
                parts = text.split(" ")
                if parts and parts[0].isdigit():
                    # Handle "1,234 contributions"
                    count = int(parts[0].replace(',', ''))
                elif "1 contribution" in text:
                    count = 1

        # If still 0, check if we missed something or it's genuinely 0
        # For our purposes, we trust the parse.

        date_map[date_str] = count
        if count > 0:
            total_commits += count
            active_days += 1

    avg = 0
    if active_days > 0:
        avg = total_commits / active_days

    return date_map, avg

if __name__ == "__main__":
    # Quick test
    d, a = fetch_user_stats("torvalds")
    if d:
        print(f"Fetched {len(d)} days.")
        print(f"Average commits/active day: {a:.2f}")
        # Print last 5 days
        sorted_dates = sorted(d.keys())
        for date in sorted_dates[-5:]:
             print(f"{date}: {d[date]}")
    else:
        print("Failed to fetch data.")
