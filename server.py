"""
Tic Tac Toe — Web Server
server.py

Flask application that exposes the existing game.py logic over HTTP.
Serves an HTML/JS front end and provides JSON endpoints for:
  - GET  /api/state          → current board state
  - POST /api/move           → player makes a move
  - POST /api/new-game       → reset the board
  - POST /api/ai-move        → AI makes a move (minimax)
  - POST /api/difficulty     → set AI difficulty (easy/medium/hard)
  - GET  /                   → serves the HTML front end

Run with:  python server.py
"""

from __future__ import annotations

import random
from typing import Optional

from flask import Flask, jsonify, request, send_from_directory

import game as g

# ── App setup ────────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder="static", template_folder="templates")

# In-memory game state (single player session for simplicity)
_board: g.Board = g.Board()
_current_player: str = "X"  # player is O, AI is X
_winner: Optional[str] = None
_draw: bool = False
_ai_enabled: bool = True
_ai_difficulty: str = "medium"  # easy | medium | hard
_player_goes_first: bool = False  # if True, player (O) goes first; AI (X) starts otherwise


def _reset_state() -> None:
    global _board, _current_player, _winner, _draw
    _board = g.Board()
    # X always goes first (traditional Tic Tac Toe rule).
    # When player goes first (_player_goes_first=True), player is X.
    # When AI goes first (_player_goes_first=False), AI is X.
    _current_player = "O" if _player_goes_first else "X"
    _winner = None
    _draw = False


def _state_dict() -> dict:
    return {
        "board": _board.cells,
        "current_player": _current_player,
        "winner": _winner,
        "draw": _draw,
        "ai_enabled": _ai_enabled,
        "ai_difficulty": _ai_difficulty,
        "player_first": _player_goes_first,
    }


# ── AI opponent (minimax with difficulty levels) ───────────────────────────────

def _minimax(board: g.Board, ai_symbol: str, is_maximizing: bool, depth: int) -> tuple[int, Optional[int]]:
    """
    Minimax with alpha-beta pruning.
    Returns (score, best_move).
    The AI plays `ai_symbol` and tries to maximize; the opponent plays the other symbol
    and tries to minimize.
    """
    winner = g.check_winner(board)
    if winner == ai_symbol:
        return (10 - depth, None)
    other_symbol = _get_other_symbol(ai_symbol)
    if winner == other_symbol:
        return (depth - 10, None)
    if g.check_draw(board):
        return (0, None)

    best_move: Optional[int] = None
    other_symbol = _get_other_symbol(ai_symbol)
    if is_maximizing:
        best_score = float("-inf")
        for move in g.get_available_moves(board):
            new_board = g.Board()
            new_board.cells = list(board.cells)
            new_board.place(move, ai_symbol)
            score, _ = _minimax(new_board, ai_symbol, False, depth + 1)
            if score > best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)
    else:
        best_score = float("inf")
        for move in g.get_available_moves(board):
            new_board = g.Board()
            new_board.cells = list(board.cells)
            new_board.place(move, other_symbol)
            score, _ = _minimax(new_board, ai_symbol, True, depth + 1)
            if score < best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)


def _get_other_symbol(symbol: str) -> str:
    """Return the other symbol."""
    return "O" if symbol == "X" else "X"


def _ai_move(board: g.Board, difficulty: str, ai_symbol: str) -> int:
    """
    Choose an AI move based on difficulty.
    - easy:   random move
    - medium: 50% optimal (minimax), 50% random
    - hard:   always optimal (minimax)
    """
    available = g.get_available_moves(board)
    if not available:
        raise ValueError("No available moves")

    if difficulty == "easy":
        return random.choice(available)

    # Determine if AI is the maximizing player (AI=X) or minimizing (AI=O)
    is_maximizing = (ai_symbol == "X")

    if difficulty == "medium":
        if random.random() < 0.5:
            _, move = _minimax(board, ai_symbol, is_maximizing, 0)
            return move if move is not None else random.choice(available)
        return random.choice(available)

    # hard: always optimal
    _, move = _minimax(board, ai_symbol, is_maximizing, 0)
    return move if move is not None else random.choice(available)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(_state_dict())


@app.route("/api/move", methods=["POST"])
def make_move():
    global _current_player, _winner, _draw

    data = request.get_json(silent=True) or {}
    cell = data.get("cell")

    if cell is None:
        return jsonify({"error": "Missing 'cell' in request body"}), 400

    try:
        cell = int(cell)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid cell number"}), 400

    if not (1 <= cell <= 9):
        return jsonify({"error": f"Cell {cell} is out of range (1-9)"}), 400

    if _winner is not None or _draw:
        return jsonify({"error": "Game is already over"}), 400

    # Determine player symbol: X when player goes first, O otherwise
    player_symbol = "X" if _player_goes_first else "O"
    ai_symbol = "O" if _player_goes_first else "X"

    if _current_player != player_symbol:
        return jsonify({"error": "It's not the player's turn"}), 400

    pos = cell - 1  # convert 1-9 to 0-8
    if not _board.place(pos, player_symbol):
        return jsonify({"error": f"Cell {cell} is already taken"}), 400

    _current_player = ai_symbol

    # Check for game end
    winner = g.check_winner(_board)
    if winner:
        _winner = winner
    elif g.check_draw(_board):
        _draw = True

    # If AI is enabled, make the AI's move
    if _ai_enabled and not _winner and not _draw:
        try:
            ai_move_result = _do_ai_move(ai_symbol)
            return jsonify({**_state_dict(), **ai_move_result})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify(_state_dict())


@app.route("/api/ai-move", methods=["POST"])
def ai_move():
    global _current_player, _winner, _draw

    if _winner is not None or _draw:
        return jsonify({"error": "Game is already over"}), 400

    # Determine AI symbol: X when player goes first, O otherwise
    ai_symbol = "X" if _player_goes_first else "O"
    player_symbol = "O" if _player_goes_first else "X"

    if _current_player != ai_symbol:
        return jsonify({"error": "It's not the AI's turn"}), 400

    try:
        move = _ai_move(_board, _ai_difficulty, ai_symbol)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    _board.place(move, ai_symbol)
    _current_player = player_symbol

    winner = g.check_winner(_board)
    if winner:
        _winner = winner
    elif g.check_draw(_board):
        _draw = True

    result = _state_dict()
    result["ai_move"] = move + 1  # return 1-9 for the front end
    return jsonify(result)


def _do_ai_move(ai_symbol: str) -> dict:
    """
    Internal helper: let the AI make one move and update state.
    Called from make_move() when AI is enabled after the player's move.
    """
    global _current_player, _winner, _draw

    if _winner is not None or _draw:
        return {}

    try:
        move = _ai_move(_board, _ai_difficulty, ai_symbol)
    except ValueError as e:
        raise

    _board.place(move, ai_symbol)
    _current_player = ai_symbol  # player already moved; now it's AI's turn in this flow

    winner = g.check_winner(_board)
    if winner:
        _winner = winner
    elif g.check_draw(_board):
        _draw = True

    result = _state_dict()
    result["ai_move"] = move + 1
    return result


@app.route("/api/new-game", methods=["POST"])
def new_game():
    _reset_state()
    return jsonify(_state_dict())


@app.route("/api/difficulty", methods=["POST"])
def set_difficulty():
    global _ai_difficulty
    data = request.get_json(silent=True) or {}
    difficulty = data.get("difficulty", "medium")
    if difficulty not in ("easy", "medium", "hard"):
        return jsonify({"error": "Invalid difficulty. Use easy, medium, or hard."}), 400
    _ai_difficulty = difficulty
    return jsonify({"ai_difficulty": difficulty})


@app.route("/api/turn-order", methods=["POST"])
def set_turn_order():
    global _player_goes_first
    data = request.get_json(silent=True) or {}
    choice = data.get("choice", "ai")  # "player" or "ai"
    if choice not in ("player", "ai"):
        return jsonify({"error": "Invalid choice. Use 'player' or 'ai'."}), 400
    _player_goes_first = (choice == "player")
    return jsonify({"player_goes_first": _player_goes_first})


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
