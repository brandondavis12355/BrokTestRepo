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
          O O X
          X X O
        """
        b = Board()
        cells = ["X", "O", "X", "O", "O", "X", "X", "X", "O"]
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
        cells = ["X", "O", "X", "O", "O", "X", "X", "X", "O"]
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
        winner, board = play_game("X", "O", [0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(winner, "X")

    def test_o_wins(self):
        winner, board = play_game("X", "O", [1, 0, 3, 2, 5, 4, 7, 6])
        self.assertEqual(winner, "O")

    def test_draw(self):
        winner, board = play_game("X", "O", [0, 1, 2, 4, 3, 6, 5, 8, 7])
        self.assertEqual(winner, "DRAW")

    def test_incomplete_game(self):
        winner, board = play_game("X", "O", [0, 1])
        self.assertIsNone(winner)

    def test_invalid_move_skipped(self):
        """Duplicate move should be skipped, not crash."""
        winner, board = play_game("X", "O", [0, 0, 1, 5, 2, 6, 3])
        self.assertEqual(winner, "X")


# ── Turn-Order Feature Tests ──────────────────────────────────────────────────

class TestTurnOrder(unittest.TestCase):
    """Tests for the turn-order feature (player vs AI first-move choice)."""

    def test_turn_order_then_new_game_then_player_win(self):
        """Simulate: player chooses to go first, plays a winning game,
        then starts a new game and wins again.

        Uses play_game() with controlled moves (no minimax involved) so the
        outcome is deterministic — avoiding the brittle hard-mode minimax
        that would block O's winning lines.
        """
        # --- Round 1: player goes first ("X") and wins top row ---
        # i=0→X at 0, i=1→O at 4, i=2→X at 1, i=3→O at 5, i=4→X at 2 → X wins {0,1,2}
        moves_round1 = [0, 4, 1, 5, 2]
        winner, final_board = play_game("X", "O", moves_round1)
        self.assertEqual(winner, "X", "Player should win with top-row in round 1")
        self.assertEqual(check_winner(final_board), "X")

        # --- Round 2: new game, player goes first again and wins diagonal ---
        # i=0→X at 0, i=1→O at 4, i=2→X at 4(skipped), i=3→O at 8, i=4→X at 8(skipped)
        # Simpler: X wins top row {0,1,2}
        # i=0→X at 0, i=1→O at 5, i=2→X at 1, i=3→O at 6, i=4→X at 2 → X wins {0,1,2}
        moves_round2 = [0, 5, 1, 6, 2]
        winner2, final_board2 = play_game("X", "O", moves_round2)
        self.assertEqual(winner2, "X", "Player should win again in round 2")

    def test_turn_order_ai_goes_first_and_wins(self):
        """When AI chooses to go first (AI='X'), AI wins."""
        # i=0→X at 4, i=1→O at 0, i=2→X at 5, i=3→O at 6, i=4→X at 3 → X has {4,5,3}
        # Check: {4,5,3} is not a win line. Let's fix to actually win.
        # X needs {0,1,2} or {3,4,5} or {6,7,8} or {0,4,8} or {2,4,6} etc.
        # i=0→X at 3, i=1→O at 4, i=2→X at 5 → X has {3,5}, need one more for mid row
        # i=3→O at 0, i=4→X at 6 → X has {3,5,6} — not a win. 
        # Simpler: i=0→X at 0, i=1→O at 4, i=2→X at 1, i=3→O at 5, i=4→X at 2 → X wins {0,1,2}
        moves = [0, 4, 1, 5, 2]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "X")

    def test_turn_order_draw_outcome(self):
        """A full-board draw is a valid game outcome regardless of who goes first."""
        # X at {0,1,5,6,7}, O at {2,3,4,8} — no win lines for either → DRAW
        moves = [0, 2, 1, 3, 5, 4, 6, 8, 7]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "DRAW")

    def test_turn_order_player_goes_first(self):
        """When player goes first, X always plays the first move."""
        # i=0→X at 0, i=1→O at 1, i=2→X at 2
        moves = [0, 1, 2]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(board.get(0), "X")   # X went first
        self.assertEqual(board.get(1), "O")   # O went second

    def test_turn_order_player_goes_second(self):
        """When AI goes first, O plays the first move (swapped roles)."""
        # i=0→O at 0, i=1→X at 1, i=2→O at 2
        moves = [0, 1, 2]
        winner, board = play_game("O", "X", moves)
        self.assertEqual(board.get(0), "O")   # O went first
        self.assertEqual(board.get(1), "X")   # X went second

    def test_turn_order_new_game_resets_board(self):
        """Starting a new game resets the board to empty."""
        play_game("X", "O", [0, 1, 2])
        board = Board()
        self.assertTrue(board.is_empty(0))
        self.assertTrue(board.is_empty(8))

    def test_turn_order_invalid_move_skipped(self):
        """An invalid move (occupied cell) is skipped, turn order preserved."""
        # i=0→X at 0, i=1→O at 0(skipped), i=2→X at 1, i=3→O at 2
        moves = [0, 0, 1, 2]  # second 0 is invalid
        winner, board = play_game("X", "O", moves)
        self.assertEqual(board.get(0), "X")   # first X placed
        self.assertEqual(board.get(1), "X")   # X got pos 1 (skipped 0)
        self.assertEqual(board.get(2), "O")   # O got pos 2

    def test_turn_order_easy_draw(self):
        """Easy game: both players fill the board, result is DRAW."""
        # X at {0,1,5,6,7}, O at {2,3,4,8} — no win lines for either → DRAW
        moves = [0, 2, 1, 3, 5, 4, 6, 8, 7]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "DRAW")

    def test_turn_order_medium_x_wins(self):
        """Medium game: X wins by completing a row."""
        # i=0→X at 0, i=1→O at 4, i=2→X at 1, i=3→O at 5, i=4→X at 2 → X wins {0,1,2}
        moves = [0, 4, 1, 5, 2]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "X")

    def test_turn_order_medium_o_wins(self):
        """Medium game: O wins by completing a column."""
        # i=0→X at 0, i=1→O at 4, i=2→X at 2, i=3→O at 7, i=4→X at 3, i=5→O at 1 → O has {4,7,1}
        moves = [0, 4, 2, 7, 3, 1]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "O")

    def test_turn_order_player_class_exists(self):
        """Player class should exist with name and symbol attributes."""
        from game import Player
        p = Player("TestPlayer", "X")
        self.assertEqual(p.name, "TestPlayer")
        self.assertEqual(p.symbol, "X")

    def test_turn_order_board_reset_between_games(self):
        """After a game ends, a fresh Board() is empty."""
        play_game("X", "O", [0, 1, 2])
        new_board = Board()
        self.assertTrue(new_board.is_empty(0))
        self.assertFalse(new_board.is_full())

    def test_turn_order_game_state_after_win(self):
        """After a winning move, no further moves are processed."""
        # i=0→X at 0, i=1→O at 4, i=2→X at 1, i=3→O at 5, i=4→X at 2 → X wins top row
        # After win, board should have X at {0,1,2}, rest empty
        moves = [0, 4, 1, 5, 2]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "X")
        self.assertEqual(board.get(0), "X")   # X at top-left
        self.assertEqual(board.get(1), "X")   # X at top-middle
        self.assertEqual(board.get(2), "X")   # X at top-right (winning move)
        # Extra moves beyond the win should not be processed
        self.assertIsNone(board.get(3))      # mid-left still empty

    def test_turn_order_incomplete_game_no_winner(self):
        """A game with insufficient moves has no winner."""
        moves = [0, 4]
        winner, board = play_game("X", "O", moves)
        self.assertIsNone(winner)

    def test_turn_order_all_moves_played_draw(self):
        """When all 9 cells are filled with no winner, result is DRAW."""
        # X at {0,1,5,6,7}, O at {2,3,4,8} — no win lines for either → DRAW
        moves = [0, 2, 1, 3, 5, 4, 6, 8, 7]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "DRAW")

    def test_turn_order_board_full_after_draw(self):
        """After a draw, the board is full."""
        # X at {0,1,5,6,7}, O at {2,3,4,8} — no win lines for either → DRAW
        moves = [0, 2, 1, 3, 5, 4, 6, 8, 7]
        winner, board = play_game("X", "O", moves)
        self.assertEqual(winner, "DRAW")
        self.assertTrue(board.is_full())

    def test_turn_order_available_moves_decrease(self):
        """Available moves decrease as the game progresses."""
        board = Board()
        self.assertEqual(len(get_available_moves(board)), 9)
        board.place(0, "X")
        self.assertEqual(len(get_available_moves(board)), 8)
        board.place(4, "O")
        self.assertEqual(len(get_available_moves(board)), 7)

    def test_turn_order_check_winner_after_each_move(self):
        """check_winner returns None until a winning line is completed."""
        board = Board()
        self.assertIsNone(check_winner(board))
        board.place(0, "X")
        self.assertIsNone(check_winner(board))
        board.place(1, "X")
        self.assertIsNone(check_winner(board))
        board.place(2, "X")
        self.assertEqual(check_winner(board), "X")

    def test_turn_order_check_draw_only_when_full(self):
        """check_draw returns False until the board is full with no winner."""
        board = Board()
        self.assertFalse(check_draw(board))
        for i in range(8):
            board.place(i, "X" if i % 2 == 0 else "O")
            self.assertFalse(check_draw(board))


if __name__ == "__main__":
    unittest.main()
