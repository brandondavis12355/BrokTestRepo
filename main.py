"""
Tic Tac Toe — CLI Interface
main.py

Player-facing entry point: menu, player input, game loop, and board display.
Depends on game.py (core logic: Board, move validation, win/draw detection).
"""

import sys
from game import Board, Player, check_winner, check_draw, WIN_LINES


# ── Display ──────────────────────────────────────────────────────────────────

def print_board(board: Board) -> None:
    """Render the 3×3 board with 1-indexed cell labels."""
    print("\n  ┌───┬───┬───┐")
    for row in range(3):
        cells = []
        for col in range(3):
            val = board.cells[row * 3 + col]
            cells.append(f" {val} " if val else " · ")
        print(f"  │{cells[0]}│{cells[1]}│{cells[2]}│")
        if row < 2:
            print("  ├───┼───┼───┤")
    print("  └───┴───┴───┘")
    print("  1 2 3  4 5 6  7 8 9")


def print_header() -> None:
    print("\n╔══════════════════════════╗")
    print("║      TIC TAC TOE        ║")
    print("╚══════════════════════════╝")


# ── Input ────────────────────────────────────────────────────────────────────

def get_move(player: Player, board: Board) -> int | None:
    """Prompt a player for a move. Returns 1–9 or None on quit."""
    while True:
        print(f"\n{player.name}'s turn ({player.symbol}) — enter a cell (1-9), or 'q' to quit:")
        raw = input("> ").strip().lower()
        if raw == "q":
            return None
        try:
            move = int(raw)
        except ValueError:
            print("  Invalid input. Enter a number 1-9.")
            continue
        if move < 1 or move > 9:
            print("  Out of range. Enter 1-9.")
            continue
        if not board.is_empty(move - 1):
            print(f"  Cell {move} is taken. Pick another.")
            continue
        return move


# ── Game loop ────────────────────────────────────────────────────────────────

def play_game() -> None:
    board = Board()
    players = [Player("Player 1", "X"), Player("Player 2", "O")]
    current = 0

    print_header()
    print_board(board)

    while True:
        move = get_move(players[current], board)
        if move is None:
            print(f"\n{players[current].name} quit. Game over.")
            return

        board.place(move - 1, players[current].symbol)
        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"\n🎉 Player {winner} wins! Final board:")
            print_board(board)
            return

        if check_draw(board):
            print("\n🤝 It's a draw!")
            print_board(board)
            return

        current = 1 - current  # switch player


# ── Menu ─────────────────────────────────────────────────────────────────────

def main() -> None:
    while True:
        print("\n── Tic Tac Toe ──")
        print("  1. Play a game")
        print("  2. Quit")
        choice = input("Choice (1/2): ").strip()
        if choice == "1":
            play_game()
        elif choice == "2":
            print("Thanks for playing! 👋")
            sys.exit(0)
        else:
            print("  Please enter 1 or 2.")


if __name__ == "__main__":
    main()
