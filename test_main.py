import unittest
from datetime import datetime, timedelta
from planner import plan_commits
from rasterizer import rasterize_text

class TestPlanner(unittest.TestCase):
    def test_plan_commits_basic(self):
        # Mock grid with single pixel at (row=6, col=51) -> This should be Today
        # Wait, the planner uses Today's row.

        today = datetime.now()
        wd = today.weekday()
        # GitHub: Sun=0. Python: Sun=6.
        today_row = 0 if wd == 6 else wd + 1

        # Create empty grid
        grid = [[False for _ in range(52)] for _ in range(7)]

        # Set pixel for Today (col 51, row today_row)
        grid[today_row][51] = True

        # Mock stats: Today has 0 commits, Avg is 5. Target = 10.
        stats = ({}, 5.0)

        # Planner
        plan = plan_commits(grid, stats, intensity_multiplier=2)

        # Expect 1 entry: today, 10 commits
        self.assertEqual(len(plan), 1, "Should plan 1 entry")
        if plan:
            today_str = today.strftime('%Y-%m-%d')
            self.assertEqual(plan[0][0], today_str)
            self.assertEqual(plan[0][1], 10)

    def test_plan_commits_existing_activity(self):
        # Mock grid with single pixel at (row=6, col=51) -> Today
        today = datetime.now()
        wd = today.weekday()
        today_row = 0 if wd == 6 else wd + 1

        grid = [[False for _ in range(52)] for _ in range(7)]
        grid[today_row][51] = True

        today_str = today.strftime('%Y-%m-%d')

        # Mock stats: Today has 8 commits, Avg is 5. Target = 10.
        stats = ({today_str: 8}, 5.0)

        plan = plan_commits(grid, stats, intensity_multiplier=2)

        # Check if plan contains today
        todays = [p for p in plan if p[0] == today_str]

        if not todays:
             self.fail("No plan generated for today")

        self.assertEqual(todays[0][1], 2, "Should add only 2 commits (10-8)")

    def test_rasterizer_i(self):
        # Font I
        # " XXX "
        # "  X  "
        # ...
        grid = rasterize_text("I")

        # The grid should be 7x52
        self.assertEqual(len(grid), 7)
        self.assertEqual(len(grid[0]), 52)

        # "I" is 5 chars wide. No padding after last char.
        # start_col = 52 - 5 = 47.
        # Cols: 47 48 49 50 51
        # Row 0: " XXX " -> F T T T F
        # Row 0 of I in font.py: " XXX "
        # col 47 corresponds to ' ' (False)
        # col 48 corresponds to 'X' (True)
        # col 49 corresponds to 'X' (True)
        # col 50 corresponds to 'X' (True)
        # col 51 corresponds to ' ' (False)

        self.assertFalse(grid[0][47], "Col 47 should be False")
        self.assertTrue(grid[0][48], "Col 48 should be True")
        self.assertTrue(grid[0][49], "Col 49 should be True")
        self.assertTrue(grid[0][50], "Col 50 should be True")
        self.assertFalse(grid[0][51], "Col 51 should be False")

        # Row 1: "  X  " -> F F T F F
        self.assertFalse(grid[1][48])
        self.assertTrue(grid[1][49])
        self.assertFalse(grid[1][50])

if __name__ == '__main__':
    unittest.main()
