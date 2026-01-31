# Tetris Clone

A classic Tetris game implementation in Python using Pygame, built with a focus on clean architecture, comprehensive testing, and property-based verification.

## Features

- Classic Tetris gameplay with all seven tetromino shapes
- Line clearing and scoring system
- Persistent high score tracking
- Clean separation between game logic and rendering
- Comprehensive test suite with property-based testing

## Requirements

- Python 3.8 or higher
- Pygame 2.5.0 or higher
- Hypothesis 6.82.0 or higher (for property-based testing)
- pytest 7.4.0 or higher (for running tests)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd try-out-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python -m tetris.main
```

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=tetris --cov-report=html --cov-report=term
```

Run only property-based tests:
```bash
pytest -k "property"
```

Run specific test file:
```bash
pytest tests/test_tetromino.py
```

## Project Structure

```
try-out-project/
├── tetris/                 # Main game package
│   ├── __init__.py
│   ├── main.py            # Entry point and game loop
│   ├── models/            # Core game logic (no Pygame dependencies)
│   │   ├── __init__.py
│   │   ├── tetromino.py   # Tetromino shapes and behavior
│   │   ├── playfield.py   # Grid state management
│   │   ├── game_state.py  # Game coordination and rules
│   │   └── high_scores.py # High score persistence
│   ├── views/             # Pygame rendering
│   │   ├── __init__.py
│   │   ├── renderer.py    # Graphics rendering
│   │   └── ui_screens.py  # Screen management
│   └── controllers/       # Input handling
│       ├── __init__.py
│       └── input_handler.py
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_tetromino.py
│   ├── test_playfield.py
│   ├── test_game_state.py
│   ├── test_high_scores.py
│   ├── test_renderer.py
│   ├── test_input_handler.py
│   ├── test_ui_manager.py
│   └── test_integration.py
├── .kiro/                 # Kiro IDE spec files
│   ├── specs/
│   │   └── tetris-clone/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   └── steering/          # Development guidelines
│       ├── architecture-patterns.md
│       ├── python-standards.md
│       ├── testing-practices.md
│       ├── pygame-patterns.md
│       └── project-context.md
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Architecture

The project follows a Modified Model-View-Controller (MVC) pattern:

- **Models** (`tetris/models/`): Pure Python game logic with no framework dependencies. This enables comprehensive testing without requiring Pygame initialization.

- **Views** (`tetris/views/`): Pygame-based rendering and UI display. Views read from models but never modify them.

- **Controllers** (`tetris/controllers/`): Input handling that translates keyboard events into game actions.

- **Main Loop** (`tetris/main.py`): Orchestrates timing, event processing, state updates, and rendering.

## Testing Strategy

The project uses a dual testing approach:

1. **Unit Tests**: Verify specific examples, edge cases, and error conditions
2. **Property-Based Tests**: Use Hypothesis to verify universal properties across all possible inputs

Each of the 27 correctness properties defined in the design document has a corresponding property test that runs 100+ iterations to ensure comprehensive coverage.

## Development

This project was developed using Kiro IDE's spec-driven development approach:

1. **Requirements**: Define acceptance criteria for all features
2. **Design**: Define architecture and correctness properties
3. **Tasks**: Break down implementation into incremental steps
4. **Implementation**: Execute tasks with continuous testing

See `.kiro/specs/tetris-clone/` for the complete specification.

## Controls

- **Left Arrow**: Move tetromino left
- **Right Arrow**: Move tetromino right
- **Space**: Rotate tetromino clockwise
- **Down Arrow**: Hard drop (instant drop to bottom)

## License

This is a learning project created to explore spec-driven development and property-based testing.
