---
inclusion: always
---

# Python Coding Standards

## Overview

This document defines the Python coding standards for the Tetris clone project. All Python code must adhere to these standards to ensure consistency, readability, and maintainability.

## Style and Formatting

### PEP 8 Compliance
- Follow PEP 8 style guide for all Python code
- Maximum line length: 100 characters (more readable for modern displays)
- Use 4 spaces for indentation (never tabs)
- Two blank lines between top-level functions and classes
- One blank line between methods within a class

### Naming Conventions
- **Classes**: PascalCase (e.g., `GameState`, `TetrominoShape`, `HighScoreManager`)
- **Functions/Methods**: snake_case (e.g., `spawn_tetromino`, `clear_rows`, `is_valid_position`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `PLAYFIELD_WIDTH`, `FALL_INTERVAL`, `MAX_HIGH_SCORES`)
- **Private methods**: Prefix with single underscore (e.g., `_calculate_score`, `_check_collision`)
- **Module names**: lowercase with underscores (e.g., `game_state.py`, `high_scores.py`)

### Import Organization
Organize imports in three groups, separated by blank lines:
1. Standard library imports
2. Third-party imports (pygame, hypothesis)
3. Local application imports

Example:
```python
import json
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pygame
from hypothesis import given, strategies as st

from models.tetromino import Tetromino
from models.playfield import Playfield
```

## Type Hints

### Required Type Hints
- All function signatures MUST include type hints for parameters and return values
- Use `Optional[Type]` for values that can be None
- Use `List[Type]`, `Tuple[Type, ...]`, `Dict[Key, Value]` for collections
- Use `-> None` for functions that don't return a value

### Examples
```python
def spawn_tetromino(self) -> Optional[Tetromino]:
    """Spawn a new tetromino at the top center."""
    pass

def get_complete_rows(self) -> List[int]:
    """Return indices of all complete rows."""
    pass

def is_valid_position(self, tetromino: Tetromino) -> bool:
    """Check if tetromino position is valid."""
    pass

def add_score(self, name: str, score: int) -> None:
    """Add a new high score entry."""
    pass
```

## Documentation

### Docstrings
- All public classes, methods, and functions MUST have docstrings
- Use triple double-quotes for docstrings
- First line: Brief one-sentence description
- Follow with detailed explanation if needed
- Document parameters, return values, and exceptions

### Docstring Format
```python
def lock_tetromino(self) -> None:
    """Lock the active tetromino into the playfield and handle consequences.
    
    This method adds the active tetromino's blocks to the playfield,
    checks for complete rows, clears them, updates the score, and
    spawns the next tetromino. If spawning fails, triggers game over.
    
    Side effects:
        - Modifies playfield grid
        - Updates score
        - Spawns new active tetromino
        - May trigger game over
    """
    pass
```

### Inline Comments
- Use comments sparingly - code should be self-documenting
- Comment WHY, not WHAT (the code shows what)
- Use comments for complex algorithms (e.g., rotation logic, line clearing)
- Keep comments up-to-date with code changes

## Code Organization

### File Structure
Each module should have a clear, single responsibility:
- `models/` - Pure Python business logic (no Pygame dependencies)
- `views/` - Pygame rendering code
- `controllers/` - Input handling
- `tests/` - All test files

### Class Structure
Organize class members in this order:
1. Class constants
2. `__init__` method
3. Public methods
4. Private methods
5. Properties (if any)

### Method Length
- Keep methods focused and short (ideally under 20 lines)
- Extract complex logic into private helper methods
- If a method does multiple things, split it

## Immutability and Pure Functions

### Prefer Immutability
- Tetromino operations (move, rotate) return NEW instances
- Don't modify objects in-place unless necessary
- Use dataclasses with `frozen=True` where appropriate

### Example
```python
def move(self, dx: int, dy: int) -> 'Tetromino':
    """Return a new tetromino moved by the given offset."""
    return Tetromino(
        shape_type=self.shape_type,
        x=self.x + dx,
        y=self.y + dy,
        rotation=self.rotation
    )
```

## Error Handling

### Validation
- Validate inputs at public API boundaries
- Raise `ValueError` for invalid arguments
- Raise `TypeError` for wrong types (though type hints help prevent this)
- Use assertions for internal invariants (things that should never happen)

### Exception Handling
- Catch specific exceptions, not bare `except:`
- Handle file I/O errors gracefully (high score persistence)
- Log errors when appropriate
- Don't silently swallow exceptions

### Example
```python
def load_high_scores(self) -> List[HighScoreEntry]:
    """Load high scores from JSON file."""
    try:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return [HighScoreEntry(**entry) for entry in data]
    except FileNotFoundError:
        # First run - no high scores yet
        return []
    except json.JSONDecodeError as e:
        # Corrupted file - log and start fresh
        print(f"Warning: Corrupted high score file: {e}")
        return []
```

## Dependencies

### Pygame Usage
- Keep Pygame code isolated in `views/` and `main.py`
- Core game logic (models/) must NOT import pygame
- This enables testing without display initialization

### Hypothesis Usage
- Use Hypothesis for property-based tests
- Define custom strategies for domain objects
- Use `@settings(max_examples=100)` for thorough testing

## Performance Considerations

### Optimization Guidelines
- Prioritize readability over premature optimization
- Profile before optimizing
- For this project, clarity > performance (it's a simple game)
- Avoid unnecessary object creation in the game loop

### Acceptable Patterns
- Pre-calculate tetromino rotation states (done once at startup)
- Cache color constants
- Reuse Pygame surfaces where possible

## Python Version

### Target Version
- Python 3.8+ (for dataclasses, type hints, walrus operator)
- Use modern Python features where they improve clarity
- Avoid deprecated features

## Code Review Checklist

Before considering code complete, verify:
- [ ] All functions have type hints
- [ ] All public APIs have docstrings
- [ ] No Pygame imports in models/
- [ ] PEP 8 compliant (line length, naming, spacing)
- [ ] No magic numbers (use named constants)
- [ ] Error cases handled appropriately
- [ ] Tests written and passing
