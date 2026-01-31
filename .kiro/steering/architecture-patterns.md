---
inclusion: always
---

# Architecture Patterns

## Overview

This document defines the architectural patterns and design principles for the Tetris clone project. Following these patterns ensures a maintainable, testable, and well-organized codebase.

## Architectural Style: Modified MVC

### Pattern Overview
The project uses a Modified Model-View-Controller (MVC) pattern adapted for game development:

- **Model** (models/): Pure Python business logic, no framework dependencies
- **View** (views/): Pygame rendering and UI display
- **Controller** (controllers/): Input handling and event processing
- **Main Loop** (main.py): Orchestrates timing, updates, and rendering

### Why This Pattern?
- **Separation of concerns**: Game logic independent of rendering
- **Testability**: Core logic can be tested without Pygame
- **Flexibility**: Easy to swap rendering engines or add new input methods
- **Clarity**: Clear boundaries between components

## Layer Responsibilities

### Models Layer (models/)

**Purpose**: Contains all game logic and business rules

**Characteristics**:
- Pure Python (no Pygame imports)
- Immutable operations where possible
- No side effects (except GameState coordination)
- 100% unit testable without display

**Modules**:
- `tetromino.py`: Tetromino shapes, rotation, movement
- `playfield.py`: Grid state, collision detection, line clearing
- `game_state.py`: Game coordination, scoring, game over logic
- `high_scores.py`: High score persistence and management

**Key Principle**: Models should never know about rendering or input

### Views Layer (views/)

**Purpose**: Handles all visual presentation using Pygame

**Characteristics**:
- Pygame-dependent code lives here
- Reads from models, never modifies them
- Stateless rendering (draws what it's told)
- No business logic

**Modules**:
- `renderer.py`: Draws game elements (playfield, tetrominoes, score)
- `ui_screens.py`: Manages different screens (start, game, game over)

**Key Principle**: Views are dumb - they display data, they don't create it

### Controllers Layer (controllers/)

**Purpose**: Translates user input into game actions

**Characteristics**:
- Processes Pygame events
- Calls model methods based on input
- No business logic (just routing)
- Stateless

**Modules**:
- `input_handler.py`: Keyboard event processing

**Key Principle**: Controllers are thin - they route, they don't decide

### Main Loop (main.py)

**Purpose**: Orchestrates the game execution

**Responsibilities**:
- Initialize all components
- Run the game loop (timing, events, updates, rendering)
- Coordinate between layers
- Handle application lifecycle

## Dependency Rules

### The Dependency Flow
```
main.py
   ↓
controllers/ → models/ ← views/
```

**Critical Rules**:
1. **Models** depend on nothing (pure Python)
2. **Views** depend on models (read-only)
3. **Controllers** depend on models (call methods)
4. **Main** depends on everything (orchestrates)

### What This Means
- ✅ Renderer can import GameState to read its state
- ✅ InputHandler can import GameState to call methods
- ❌ GameState CANNOT import Renderer or InputHandler
- ❌ Tetromino CANNOT import pygame

### Enforcing Dependencies
If you find yourself wanting to import pygame in models/:
- **Stop** - you're breaking the architecture
- **Refactor** - move that code to views/
- **Pass data** - models return data, views render it

## Data Flow

### Typical Game Loop Iteration
```
1. Input: User presses key
   → InputHandler processes event
   → Calls GameState.move_active_left()

2. Update: Time passes
   → Main calculates delta_time
   → Calls GameState.update(delta_time)
   → GameState moves tetromino down if interval elapsed

3. Render: Display current state
   → Main calls Renderer.render_game(game_state)
   → Renderer reads game_state properties
   → Draws to screen
```

### Key Insight
Data flows in one direction per phase:
- **Input phase**: Events → Controllers → Models
- **Update phase**: Time → Models (internal state changes)
- **Render phase**: Models → Views → Screen

## Immutability Patterns

### When to Use Immutability
- **Tetromino operations**: Always return new instances
- **Value objects**: Use frozen dataclasses
- **Configuration**: Constants never change

### Example: Immutable Tetromino
```python
class Tetromino:
    def move(self, dx: int, dy: int) -> 'Tetromino':
        """Return NEW tetromino at moved position."""
        return Tetromino(
            shape_type=self.shape_type,
            x=self.x + dx,
            y=self.y + dy,
            rotation=self.rotation
        )
```

**Benefits**:
- Easier to reason about (no hidden state changes)
- Safer for concurrent operations
- Simpler testing (no setup/teardown of state)

### When Mutability is OK
- **GameState**: Coordinates multiple objects, mutability is practical
- **Playfield**: Grid state changes frequently, copying is expensive
- **HighScoreManager**: Manages a list that grows/shrinks

**Rule of Thumb**: Prefer immutability for small objects, accept mutability for coordinators

## State Management

### Game State Ownership
- **GameState** owns the authoritative game state
- **Playfield** owns the grid state
- **HighScoreManager** owns the high score list
- **UIManager** owns the current screen state

### State Access Patterns
- **Read**: Components can read state via public properties/methods
- **Write**: Only the owner modifies its state
- **Coordination**: GameState coordinates between components

### Example: Who Owns What
```python
class GameState:
    def __init__(self):
        self.playfield = Playfield()        # GameState owns playfield
        self.active_tetromino = None        # GameState owns active piece
        self.score = 0                      # GameState owns score
        self.game_over = False              # GameState owns game over flag
```

## Error Handling Strategy

### Validation at Boundaries
- Validate inputs at public API entry points
- Raise exceptions for invalid inputs
- Use type hints to prevent type errors

### Graceful Degradation
- File I/O errors: Log and continue with defaults
- Pygame errors: Fail fast with clear error message
- Invalid game states: Assert and log (should never happen)

### Error Propagation
- Let exceptions bubble up from models
- Catch and handle at the appropriate level
- Don't silently swallow errors

## Testing Architecture

### Test Organization Mirrors Code
```
tetris/models/game_state.py
   ↓
tests/test_game_state.py
```

### Testing Each Layer
- **Models**: Unit tests + property tests (no mocks needed)
- **Views**: Unit tests with mocked Pygame surfaces
- **Controllers**: Unit tests with mocked game state
- **Integration**: End-to-end tests with all components

### Dependency Injection for Testing
Pass dependencies explicitly to enable testing:
```python
# Good - testable
class Renderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface

# Bad - hard to test
class Renderer:
    def __init__(self):
        self.surface = pygame.display.set_mode((800, 600))
```

## File Organization

### Directory Structure
```
tetris/
├── __init__.py
├── main.py                    # Entry point and game loop
├── models/                    # Business logic layer
│   ├── __init__.py
│   ├── tetromino.py
│   ├── playfield.py
│   ├── game_state.py
│   └── high_scores.py
├── views/                     # Presentation layer
│   ├── __init__.py
│   ├── renderer.py
│   └── ui_screens.py
└── controllers/               # Input layer
    ├── __init__.py
    └── input_handler.py

tests/                         # Test suite
├── __init__.py
├── strategies.py              # Hypothesis strategies
├── test_tetromino.py
├── test_playfield.py
├── test_game_state.py
├── test_high_scores.py
├── test_renderer.py
├── test_input_handler.py
├── test_ui_manager.py
└── test_integration.py
```

### Module Size Guidelines
- Keep modules focused (single responsibility)
- Aim for 200-400 lines per module
- Split if a module exceeds 500 lines
- Each module should have a clear purpose

## Constants and Configuration

### Where to Define Constants
- **Module-level constants**: Define at top of module where used
- **Shared constants**: Define in the module that owns the concept
- **Configuration**: Consider a separate config module if it grows

### Example: Playfield Constants
```python
# models/playfield.py
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20

class Playfield:
    def __init__(self):
        self.width = PLAYFIELD_WIDTH
        self.height = PLAYFIELD_HEIGHT
```

### Example: Rendering Constants
```python
# views/renderer.py
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
PLAYFIELD_OFFSET_X = 250
PLAYFIELD_OFFSET_Y = 50
```

## Performance Considerations

### Optimization Strategy
1. **Make it work** (correctness first)
2. **Make it right** (clean code)
3. **Make it fast** (only if needed)

### For This Project
- Performance is not a concern (simple 2D game)
- Prioritize clarity over optimization
- Pre-calculate rotation states (done once)
- Avoid unnecessary object creation in game loop

### When to Optimize
- Profile first (don't guess)
- Optimize hot paths only
- Measure before and after
- Document why optimization was needed

## Extensibility Points

### Designed for Extension
The architecture makes these extensions easy:
- **New tetromino shapes**: Add to tetromino.py shape definitions
- **Different fall speeds**: Modify GameState.fall_interval
- **New input methods**: Add new controller
- **Different renderers**: Implement new view (terminal, web, etc.)
- **AI players**: Create new controller that calls GameState methods

### Extension Example: Adding a New Renderer
```python
# views/terminal_renderer.py
class TerminalRenderer:
    def render_game(self, game_state: GameState) -> None:
        """Render game state to terminal using ASCII."""
        # Read from game_state, print to terminal
        # No changes needed to models/
```

## Anti-Patterns to Avoid

### ❌ God Objects
Don't create one class that does everything:
```python
# Bad
class Game:
    def __init__(self):
        # Handles rendering, input, logic, persistence...
```

### ❌ Circular Dependencies
Don't create circular imports:
```python
# Bad
# game_state.py imports renderer.py
# renderer.py imports game_state.py
```

### ❌ Leaky Abstractions
Don't let implementation details leak:
```python
# Bad - Pygame leaking into models
class Tetromino:
    def render(self, surface: pygame.Surface):
        # Tetromino shouldn't know about rendering!
```

### ❌ Hidden State
Don't modify state in unexpected places:
```python
# Bad - Renderer modifying game state
class Renderer:
    def render_game(self, game_state: GameState):
        game_state.score += 10  # NO! Renderer should only read!
```

## Architecture Review Checklist

Before considering architecture complete:
- [ ] Models have no Pygame dependencies
- [ ] Views only read from models, never modify
- [ ] Controllers are thin routing layers
- [ ] Dependencies flow in correct direction
- [ ] Each module has single, clear responsibility
- [ ] State ownership is clear and documented
- [ ] Error handling strategy is consistent
- [ ] Testing strategy aligns with architecture
- [ ] Extension points are identified
- [ ] No circular dependencies
