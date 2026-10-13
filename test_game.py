"""
Tic Tac Toe — Unit Tests
test_game.py

Covers: Board, check_winner, check_draw, get_available_moves, play_game.
Run: python -m pytest test_game.py -v
"""

import unittest
from game import Board, check_winner, check_draw, get_available_moves, play_game, WIN_LINES


class TestBoard(unittest.TestCase):
    def test_empty_board(self):
        b = Board()
        self.assertEqual(b.cells, [None] * 9)
        self.assertFalse(b.is_full())
        self.assertTrue(b.is_empty(0))

    def test_place_and_get(self):
        b = Board()
        self.assertTrue(b.place(0, "X"))
        self.assertEqual(b.get(0), "X")
        self.assertFalse(b.is_empty(0))

    def test_place_occupied_returns_false(self):
        b = Board()
        b.place(3, "X")
        self.assertFalse(b.place(3, "O"))

    def test_place_out_of_range(self):
        b = Board()
        self.assertFalse(b.place(-1, "X"))
        self.assertFalse(b.place(9, "X"))

    def test_get_out_of_range(self):
        b = Board()
        self.assertIsNone(b.get(-1))
        self.assertIsNone(b.get(9))

    def test_reset(self):
        b = Board()
        b.place(0, "X")
        b.reset()
        self.assertEqual(b.cells, [None] * 9)

    def test_is_full(self):
        b = Board()
        for i in range(9):
            b.place(i, "X" if i % 2 == 0 else "O")
        self.assertTrue(b.is_full())

    def test_display(self):
        b = Board()
        b.place(0, "X")
        b.place(1, "O")
        d = b.display()
        self.assertIn("X", d)
        self.assertIn("O", d)
        self.assertIn(".", d)


class TestCheckWinner(unittest.TestCase):
    def test_no_winner_empty(self):
        b = Board()
        self.assertIsNone(check_winner(b))

    def test_x_wins_top_row(self):
        b = Board()
        b.place(0, "X"); b.place(1, "X"); b.place(2, "X")
        self.assertEqual(check_winner(b), "X")

    def test_o_wins_diagonal(self):
        b = Board()
        b.place(0, "O"); b.place(4, "O"); b.place(8, "O")
        self.assertEqual(check_winner(b), "O")

    def test_x_wins_middle_col(self):
        b = Board()
        b.place(1, "X"); b.place(4, "X"); b.place(7, "X")
        self.assertEqual(check_winner(b), "X")

    def test_o_wins_bottom_row(self):
        b = Board()
        b.place(6, "O"); b.place(7, "O"); b.place(8, "O")
        self.assertEqual(check_winner(b), "O")

    def test_no_winner_partial(self):
        b = Board()
        b.place(0, "X"); b.place(1, "O"); b.place(2, "X")
        self.assertIsNone(check_winner(b))

    def test_full_board_no_winner(self):
        """
        Full board with no winner should return None.
        Layout:
          X O X
          O X O
          X O X
        """
        b = Board()
        cells = ["X", "O", "X", "O", "X", "O", "X", "O", "X"]
        b.cells = cells
        w = check_winner(b)
        self.assertIsNone(w, f"full board with no winner should have no winner, got {w}")

    def test_all_win_lines_covered(self):
        """Verify all 8 WIN_LINES produce a winner when filled."""
        for a, b_idx, c in WIN_LINES:
            b = Board()
            b.place(a, "X")
            b.place(b_idx, "X")
            b.place(c, "X")
            self.assertEqual(check_winner(b), "X", f"Line ({a},{b_idx},{c}) should win")


class TestCheckDraw(unittest.TestCase):
    def test_draw_full_board_no_winner(self):
        b = Board()
        cells = ["X", "O", "X", "O", "X", "O", "X", "O", "X"]
        b.cells = cells
        self.assertTrue(check_draw(b))

    def test_not_draw_if_winner(self):
        b = Board()
        b.place(0, "X"); b.place(1, "X"); b.place(2, "X")
        self.assertFalse(check_draw(b))

    def test_not_draw_if_not_full(self):
        b = Board()
        b.place(0, "X")
        self.assertFalse(check_draw(b))


class TestGetAvailableMoves(unittest.TestCase):
    def test_empty_board_all_available(self):
        b = Board()
        self.assertEqual(get_available_moves(b), list(range(9)))

    def test_some_moves_taken(self):
        b = Board()
        b.place(0, "X")
        b.place(4, "O")
        moves = get_available_moves(b)
        self.assertNotIn(0, moves)
        self.assertNotIn(4, moves)
        self.assertEqual(len(moves), 7)

    def test_full_board_no_moves(self):
        b = Board()
        for i in range(9):
            b.place(i, "X" if i % 2 == 0 else "O")
        self.assertEqual(get_available_moves(b), [])


class TestPlayGame(unittest.TestCase):
    def test_x_wins(self):
        winner, board = play_game("X", "O", [0, 1, 2, 3, 4])
        self.assertEqual(winner, "X")

    def test_o_wins(self):
        winner, board = play_game("X", "O", [0, 1, 3, 4, 5])
        self.assertEqual(winner, "O")

    def test_draw(self):
        winner, board = play_game("X", "O", [0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(winner, "DRAW")

    def test_incomplete_game(self):
        winner, board = play_game("X", "O", [0, 1])
        self.assertIsNone(winner)

    def test_invalid_move_skipped(self):
        """Duplicate move should be skipped, not crash."""
        winner, board = play_game("X", "O", [0, 0, 1, 2, 3])
        self.assertEqual(winner, "X")


if __name__ == "__main__":
    unittest.main()
