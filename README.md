# Tic Tac Toe

<div align="center">

A modern, fully-featured **Tic Tac Toe** game built in Python — available as both a **CLI** and a **web application**.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/tests-46%2F46-passing-brightgreen.svg)](test_game.py)

</div>

---

## Features

| Feature | Description |
| --- | --- |
| 🎮 **Two Modes** | Play locally via the terminal or challenge an AI opponent through a web browser |
| 🤖 **AI Opponent** | Smart minimax-based AI with three difficulty levels (easy, medium, hard) |
| 🏆 **Win & Draw Detection** | Automatic detection of winning lines and draws after every move |
| 📱 **Responsive Web UI** | Clean, interactive HTML/JS frontend with real-time game state updates |
| ✅ **Tested** | Comprehensive unit test suite covering all game logic (46 tests) |

---

## Project Structure

```
BrokTestRepo/
├── README.md          # This file — project overview and documentation
├── game.py            # Core game logic (Board class, win/draw detection)
├── main.py            # CLI interface (menu, player input, game loop)
├── server.py          # Flask web server exposing game logic via REST API
├── test_game.py       # Unit tests for game.py — 46 tests
└── templates/
    └── index.html     # Web UI template with embedded game logic
```

---

## Setup

### Prerequisites

- **Python 3.6+** (standard library only for CLI mode)
- **Flask** (required for web mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/brandondavis12355/BrokTestRepo.git
cd BrokTestRepo

# Install Flask (for web mode)
pip install flask
```

---

## Usage

### CLI Mode

Play against a friend on the same machine:

```bash
python main.py
```

Follow the menu prompts to start a new game, enter moves (1–9), and see results.

### Web Mode

Start the Flask server and play in your browser:

```bash
python server.py
```

Then open **http://localhost:5000** in your web browser. You can choose to go first (as **X**) or let the AI go first, and select from three difficulty levels.

---

## How to Play

1. The board is a 3×3 grid numbered 1–9:

   ```
    1 | 2 | 3
   -----------
    4 | 5 | 6
   -----------
    7 | 8 | 9
   ```

2. Players take turns entering a number to place their mark (**X** or **O**).
3. The first player to get three in a row (horizontally, vertically, or diagonally) wins.
4. If all nine cells are filled with no winner, the game is a draw.

---

## Testing

Run the full test suite:

```bash
python -m pytest test_game.py
# or
python -m unittest test_game
```

All **46 tests** pass (100% coverage):

```
============================= 46 passed in 0.03s ==============================
```

The test suite covers:

- **Board initialization** — empty board, move validation
- **Win detection** — all 8 possible winning lines (3 rows, 3 columns, 2 diagonals)
- **Draw detection** — full board with no winner
- **Turn order** — player/AI alternation, go-first/go-second logic
- **Edge cases** — invalid moves, game-over states, board resets

---

## Game Logic Overview

| Component | Details |
| --- | --- |
| **Board** | A 3×3 grid represented as a flat list of 9 cells (`[None] * 9`) |
| **Players** | `X` and `O` — either player can go first via the web UI |
| **AI** | Minimax algorithm with alpha-beta pruning; easy (random), medium (50/50), hard (always optimal) |
| **Winning lines** | All 8 possible lines checked after every move |
| **Draw detection** | Triggered when all cells are filled and no player has won |

---

## API Endpoints (Web Server)

| Endpoint       | Method | Description                          |
| -------------- | ------ | ------------------------------------ |
| `GET /api/state`       | GET    | Get current game state               |
| `POST /api/new-game`   | POST   | Reset the game board                 |
| `POST /api/turn-order` | POST   | Choose who goes first (player/AI)    |
| `POST /api/move`       | POST   | Make a move at a given position      |
| `POST /api/ai-move`    | POST   | Trigger AI to make its move          |
| `POST /api/difficulty` | POST   | Set AI difficulty (easy/medium/hard) |

---

## Development

- **game.py** — Core `Board` class with all game logic. No external dependencies.
- **main.py** — CLI entry point with menu system and interactive gameplay.
- **server.py** — Flask REST API wrapping `game.py`; serves the web UI.
- **test_game.py** — Unit tests using `unittest` / `pytest`.
- **templates/index.html** — Self-contained HTML/JS frontend communicating via fetch API.

---

## License

MIT
