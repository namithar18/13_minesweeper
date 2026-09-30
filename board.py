import random

DEFAULT_ROWS = 6
DEFAULT_COLS = 6
DEFAULT_MINES = 6

# Difficulty presets — all in memory, no external file needed.
# Keys are the single-letter shortcuts accepted at startup.
DIFFICULTY = {
    "e": {"label": "Easy",   "rows":  6, "cols":  6, "mines":  6},
    "m": {"label": "Medium", "rows": 10, "cols": 10, "mines": 15},
    "h": {"label": "Hard",   "rows": 14, "cols": 14, "mines": 35},
}


class Board:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, mines=DEFAULT_MINES):
        self.rows = rows
        self.cols = cols
        self.mine_total = mines
        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()

    def _build_mines(self):
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        return set(random.sample(cells, self.mine_total))

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def adjacent_mines(self, r, c):
        return sum(pos in self.mines for pos in self.neighbors(r, c))

    def reveal(self, start):
        """Flood-fill reveal starting from start.

        Returns True if a mine was hit, False otherwise.
        Mine cells are never added to self.revealed so that won() stays accurate.
        Flagged cells are skipped (both as start and during expansion).
        """
        if start in self.flags:
            return False
        stack = [start]
        hit_mine = False
        while stack:
            pos = stack.pop()
            if pos in self.revealed or pos in self.flags:
                continue
            if pos in self.mines:
                hit_mine = True
                continue
            r, c = pos
            self.revealed.add(pos)
            if self.adjacent_mines(r, c) == 0:
                stack.extend(n for n in self.neighbors(r, c) if n not in self.revealed)
        return hit_mine

    def toggle_flag(self, pos):
        """Toggle a flag on an unrevealed cell.

        Returns 'placed', 'removed', or None if the cell is already revealed.
        """
        if pos in self.revealed:
            return None
        if pos in self.flags:
            self.flags.remove(pos)
            return 'removed'
        self.flags.add(pos)
        return 'placed'

    def won(self):
        return len(self.revealed) == self.rows * self.cols - self.mine_total
