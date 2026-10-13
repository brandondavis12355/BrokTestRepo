"""
Tic Tac Toe — core game logic.

Board is a 3x3 grid represented as a flat list of 9 cells.
Each cell holds 'X', 'O', or None (empty).
"""

from typing import List, Optional, Tuple


class Board:
    """3x3 Tic Tac Toe board."""

    SIZE = 3
    CELLS = 9

    def __init__(self) -> None:
        self.cells: List[Optional[str]] = [None] * self.CELLS

    def reset(self) -> None:
        self.cells = [None] * self.CELLS

    def is_empty(self, pos: int) -> bool:
        """Return True if the given position (0-8) is unoccupied."""
        return self.cells[pos] is None

    def is_full(self) -> bool:
        """Return True if every cell is occupied."""
        return all(c is not None for c in self.cells)

    def place(self, pos: int, mark: str) -> bool:
        """
        Place `mark` ('X' or 'O') at position `pos` (0-8).
        Returns True on success, False if the cell is occupied or pos is out of range.
        """
        if not (0 <= pos < self.CELLS):
            return False
        if self.cells[pos] is not None:
            return False
        self.cells[pos] = mark
        return True

    def get(self, pos: int) -> Optional[str]:
        """Return the mark at position `pos`, or None if empty / out of range."""
        if 0 <= pos < self.CELLS:
            return self.cells[pos]
        return None

    def display(self) -> str:
        """Return a human-readable string representation of the board."""
        lines = []
        for row in range(self.SIZE):
            cells = []
            for col in range(self.SIZE):
                idx = row * self.SIZE + col
                cells.append(self.cells[idx] or ".")
            lines.append(" | ".join(cells))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Board({self.cells!r})"


# Win lines: all 8 winning index combinations on a 3x3 board.
WIN_LINES: List[Tuple[int, int, int]] = (
    (0, 1, 2),  # top row
    (3, 4, 5),  # middle row
    (6, 7, 8),  # bottom row
    (0, 3, 6),  # left col
    (1, 4, 7),  # middle col
    (2, 5, 8),  # right col
    (0, 4, 8),  # diagonal ↘
    (2, 4, 6),  # diagonal ↙
)


def check_winner(board: Board) -> Optional[str]:
    """
    Return 'X', 'O', or None.
    Returns the winning mark if a line of 3 is found, None otherwise.
    """
    for a, b, c in WIN_LINES:
        mark = board.cells[a]
        if mark is not None and board.cells[b] == mark and board.cells[c] == mark:
            return mark
    return None


def check_draw(board: Board) -> bool:
    """Return True if the board is full and no winner exists."""
    return board.is_full() and check_winner(board) is None


def get_available_moves(board: Board) -> List[int]:
    """Return a list of empty cell positions (0-8)."""
    return [i for i, c in enumerate(board.cells) if c is None]


def play_game(
    player1: str = "X",
    player2: str = "O",
    moves: List[int] = None,
) -> Tuple[Optional[str], Board]:
    """
    Simulate a game given a sequence of moves (positions 0-8).
    Players alternate: player1 first, then player2, etc.

    Returns (winner, final_board).
    winner is 'X', 'O', 'DRAW', or None if the game is incomplete.
    """
    board = Board()
    if moves is None:
        moves = []

    for i, pos in enumerate(moves):
        mark = player1 if i % 2 == 0 else player2
        if not board.place(pos, mark):
            # Invalid move — skip it (already occupied or out of range)
            continue
        winner = check_winner(board)
        if winner is not None:
            return winner, board
        if board.is_full():
            return "DRAW", board

    return None, board
