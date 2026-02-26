from font import FONT_5X7

def rasterize_text(text):
    """
    Converts a string of text into a 7x52 boolean matrix.
    The text is right-aligned.
    """
    height = 7
    width = 52

    # Initialize empty grid (7 rows, 52 cols)
    grid = [[False for _ in range(width)] for _ in range(height)]

    # Build the full bitmap for the text
    full_bitmap = [[] for _ in range(height)]

    for char_idx, char in enumerate(text.upper()):
        if char in FONT_5X7:
            char_lines = FONT_5X7[char]
        else:
            char_lines = FONT_5X7[' '] # Default to space for unknown chars

        for i in range(height):
            # Convert "X" to True, " " to False
            row_bools = [c == 'X' for c in char_lines[i]]
            full_bitmap[i].extend(row_bools)

            # Add 1 pixel spacing between characters, unless it's the last one
            if char_idx < len(text) - 1:
                full_bitmap[i].append(False)

    # Calculate starting column to right-align
    text_width = len(full_bitmap[0])
    start_col = width - text_width

    # Fill the grid
    for r in range(height):
        for c in range(text_width):
            grid_col = start_col + c
            if 0 <= grid_col < width:
                grid[r][grid_col] = full_bitmap[r][c]

    return grid

def print_grid(grid):
    """Helper to print the grid to console for verification."""
    for row in grid:
        line = ""
        for cell in row:
            line += "█" if cell else "."
        print(line)
