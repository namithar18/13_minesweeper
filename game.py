from board import Board, DIFFICULTY


class Minesweeper:
    def __init__(self):
        preset = self._choose_difficulty()
        self.board = Board(
            rows=preset["rows"],
            cols=preset["cols"],
            mines=preset["mines"],
        )

    # ------------------------------------------------------------------
    # Difficulty selection
    # ------------------------------------------------------------------

    def _choose_difficulty(self):
        """Prompt the player to pick a difficulty and return its preset dict."""
        print("Minesweeper")
        print("Select difficulty:  e = Easy (6x6, 6 mines)")
        print("                    m = Medium (10x10, 15 mines)")
        print("                    h = Hard (14x14, 35 mines)")
        while True:
            choice = input("Difficulty [e/m/h]: ").strip().lower()
            if choice in DIFFICULTY:
                preset = DIFFICULTY[choice]
                print(f"{preset['label']} selected.")
                return preset
            print("Please enter e, m, or h.")

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display(self, reveal_mines=False):
        b = self.board
        # Column header — pad to match the row-number prefix width
        col_width = len(str(b.cols))
        row_prefix = " " * (col_width + 2)
        print("\n" + row_prefix + " ".join(f"{c + 1:{col_width}}" for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(ch)
            print(f"{r + 1:{col_width}} " + " ".join(f"{ch:{col_width}}" for ch in cells))

    # ------------------------------------------------------------------
    # Main game loop
    # ------------------------------------------------------------------

    def run(self):
        b = self.board
        print(f"Commands: r row col | f row col | q   (board: {b.rows}x{b.cols}, {b.mine_total} mines)")
        while True:
            self.display()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            if parts[0] == "f":
                result = self.board.toggle_flag((r, c))
                if result == "placed":
                    print("Flag placed.")
                elif result == "removed":
                    print("Flag removed.")
                else:
                    print("Cannot flag a revealed cell.")
                continue

            pos = (r, c)
            if pos in self.board.flags:
                print("Remove the flag first.")
                continue
            if pos in self.board.revealed:
                print("Already revealed.")
                continue

            if self.board.reveal(pos):
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return
            if self.board.won():
                self.display()
                print("You cleared the board!")
                return
