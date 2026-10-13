# BrokTestRepo

## Tic Tac Toe

A simple two-player Tic Tac Toe game implemented in Python.

## Project Structure

```
BrokTestRepo/
├── README.md       # This file
├── game.py         # Core game logic (board, move validation, win/draw detection)
├── main.py         # CLI interface (menu, player input, game loop, display)
└── test_game.py    # Unit tests for game logic
```

## Setup

No external dependencies required. Python 3.6+ is sufficient.

```bash
# Clone the repository
git clone https://github.com/brandondavis12355/BrokTestRepo.git
cd BrokTestRepo
```

## Usage

Run the game from the command line:

```bash
python main.py
```

The game supports two players taking turns on a 3×3 board. Players enter a number (1–9) to place their mark. The game detects wins and draws automatically.

### Board Layout

```
 1 | 2 | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9
```

## Testing

Run the unit test suite:

```bash
python -m pytest test_game.py
# or
python -m unittest test_game
```

## Development

- **game.py** — Core game logic: board representation, move validation, win/draw detection
- **main.py** — CLI interface: menu, player input, game loop, board display
- **test_game.py** — Unit tests covering all game logic

## License

MIT
