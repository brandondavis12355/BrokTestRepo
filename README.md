# BrokTestRepo

## Tic Tac Toe

A modern, fully-featured **Tic Tac Toe** game built in Python — available as both a **CLI** and a **web application**.

---

### Features

- 🎮 **Two modes**: Play locally via the terminal or challenge an AI opponent through a web browser
- 🤖 **AI opponent**: The server runs a smart AI that plays as "O" against your "X"
- 🏆 **Win & draw detection**: Automatic detection of winning lines and draws
- 📱 **Responsive web UI**: Clean, interactive HTML/JS frontend with real-time game state updates
- ✅ **Tested**: Comprehensive unit test suite covering all game logic

---

### Project Structure

```
BrokTestRepo/
├── README.md          # This file — project overview and documentation
├── game.py            # Core game logic (Board class, win/draw detection)
├── main.py            # CLI interface (menu, player input, game loop)
├── server.py          # Flask web server exposing game logic via REST API
├── test_game.py       # Unit tests for game.py — 27 tests
└── templates/
    └── index.html     # Web UI template with embedded game logic
```

---

### Setup

No external dependencies required beyond Python 3.6+. The Flask web server is included in the project.

```bash
# Clone the repository
git clone https://github.com/brandondavis12355/BrokTestRepo.git
cd BrokTestRepo
```

#### Install Flask (for web mode)

```bash
pip install flask
```

---

### Usage

#### CLI Mode

Play against a friend on the same machine:

```bash
python main.py
```

Follow the menu prompts to start a new game, enter moves (1–9), and see results.

#### Web Mode

Start the Flask server and play in your browser:

```bash
python server.py
```

Then open `http://localhost:5000` in your web browser. You can choose to go first (as **X**) or let the AI go first.

---

### How to Play

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

### Testing

Run the full test suite:

```bash
python -m pytest test_game.py
# or
python -m unittest test_game
```

The test suite covers board initialization, move validation, win detection for all lines, draw detection, and edge cases.

---

### Game Logic Overview

- **Board**: A 3×3 grid represented as a flat list of 9 cells (`[None] * 9`).
- **Players**: `X` always goes first; `O` is the second player (or AI).
- **Winning lines**: All 8 possible lines (3 rows, 3 columns, 2 diagonals) are checked after each move.
- **Draw detection**: A draw occurs when all cells are filled and no player has won.

---

### API Endpoints (Web Server)

| Endpoint       | Method | Description                          |
| -------------- | ------ | ------------------------------------ |
| `/state`       | GET    | Get current game state               |
| `/reset`       | POST   | Reset the game board                 |
| `/turn-order`  | POST   | Choose who goes first (player/AI)    |
| `/move`        | POST   | Make a move at a given position      |

---

### Development

- **game.py** — Core `Board` class with all game logic. No external dependencies.
- **main.py** — CLI entry point with menu system and interactive gameplay.
- **server.py** — Flask REST API wrapping `game.py`; serves the web UI.
- **test_game.py** — Unit tests using `unittest` / `pytest`.
- **templates/index.html** — Self-contained HTML/JS frontend communicating via fetch API.

---

### License

MIT
