from datetime import datetime, timedelta

def plan_commits(raster_grid, user_stats, intensity_multiplier=2):
    """
    Generates a list of commit operations.

    Args:
        raster_grid (list[list[bool]]): 7x52 boolean matrix.
        user_stats (tuple): (date_map, average)
            date_map: Dictionary mapping 'YYYY-MM-DD' to current commit count.
            average: float, average commits on active days.
        intensity_multiplier (float): Multiplier for the target commit count.

    Returns:
        list[tuple]: List of (date_str, commits_to_add)
    """
    date_map, average = user_stats

    if average == 0:
        target_commits = 5 # Default if no history
    else:
        target_commits = int(average * intensity_multiplier)

    today = datetime.now()
    plan = []

    def get_github_row(dt):
        # GitHub Row 0 = Sunday.
        # Python 6 = Sunday.
        wd = dt.weekday() # Mon=0...Sun=6
        if wd == 6: return 0
        return wd + 1

    today_row = get_github_row(today)

    # We iterate through the grid.
    # The grid is 7 rows x 52 cols.
    # GitHub graph fills columns (weeks) from left to right.
    # The last column (index 51) corresponds to the current week.

    for col in range(52):
        for row in range(7):
            # Calculate how many days back this cell is from Today.
            # Grid (51, today_row) is Today (0 days ago).
            # Grid (51, today_row - 1) is Yesterday (1 day ago).
            # Grid (51, today_row + 1) is Tomorrow (-1 days ago, future).

            # The weeks difference: (51 - col)
            # The days difference within the week: (today_row - row)

            days_ago = ((51 - col) * 7) + (today_row - row)

            if days_ago < 0:
                # Future date
                continue

            target_date = today - timedelta(days=days_ago)
            date_str = target_date.strftime('%Y-%m-%d')

            if raster_grid[row][col]:
                current_count = date_map.get(date_str, 0)
                commits_needed = max(0, target_commits - current_count)

                if commits_needed > 0:
                    plan.append((date_str, commits_needed))

    return plan

if __name__ == "__main__":
    # Test
    mock_avg = 5.0
    today_str = datetime.now().strftime('%Y-%m-%d')
    mock_map = {today_str: 5}

    # Mock grid (all true for testing)
    mock_grid = [[True] * 52 for _ in range(7)]

    plan = plan_commits(mock_grid, (mock_map, mock_avg), 2)
    print(f"Generated plan with {len(plan)} entries.")

    todays = [p for p in plan if p[0] == today_str]
    # Expectation: Target = 5 * 2 = 10. Current = 5. Needed = 5.
    print(f"Plan for today ({today_str}): {todays}")
