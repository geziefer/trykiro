# Design Document: Tetris Clone

## Overview

This design document outlines the technical architecture for a classic Tetris clone implemented in Python using Pygame. The implementation follows a clean separation between game logic (model), rendering (view), and input handling (controller), ensuring the core game state is independent of Pygame-specific code. This separation enables comprehensive testing of game logic without requiring graphical rendering.

The system is organized into distinct modules:
- **Core game logic**: Pure Python classes managing game state, tetromino behavior, and rules
- **Rendering layer**: Pygame-based graphics rendering
- **Input handling**: Keyboard event processing
- **Persistence layer**: JSON-based high score storage
- **UI management**: Screen transitions and state management

## Architecture

### High-Level Architecture

The application follows a modified Model-View-Controller (MVC) pattern adapted for game development:

```
┌─────────────────────────────────────────────────────────┐
│                     Main Game Loop                       │
│  (Timing, Event Processing, State Updates, Rendering)   │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼─────┐
│ Model  │      │   View   │
│ (Core  │◄─────┤ (Pygame  │
│ Logic) │      │ Renderer)│
└───▲────┘      └──────────┘
    │
┌───┴────────┐
│ Controller │
│  (Input    │
│  Handler)  │
└────────────┘
```

### Module Structure

```
tetris/
├── main.py                 # Entry point, main game loop
├── models/
│   ├── __init__.py
│   ├── tetromino.py       # Tetromino shapes and rotation logic
│   ├── playfield.py       # 10x20 grid state management
│   ├── game_state.py      # Core game state and rules
│   └── high_scores.py     # High score persistence
├── views/
│   ├── __init__.py
│   ├── renderer.py        # Pygame rendering logic
│   └── ui_screens.py      # Start, game, game over screens
├── controllers/
│   ├── __init__.py
│   └── input_handler.py   # Keyboard input processing
└── tests/
    ├── __init__.py
    ├── test_tetromino.py
    ├── test_playfield.py
    ├── test_game_state.py
    └── test_high_scores.py
```

## Components and Interfaces

### 1. Tetromino (models/tetromino.py)

**Purpose**: Represents individual tetromino pieces with their shape, color, position, and rotation state.

**Key Attributes**:
- Shape type: One of seven types ('I', 'L', 'J', 'O', 'S', 'Z', 'T')
- Color: RGB color tuple specific to each shape type
- Position: (x, y) grid coordinates
- Rotation: 0-3 representing 90-degree increments
- Blocks: List of relative block positions

**Key Behaviors**:
- Rotate clockwise: Return new tetromino rotated 90° (immutable operation)
- Move: Return new tetromino moved by offset (immutable operation)
- Get absolute blocks: Calculate block positions in grid coordinates
- Get shape matrix: Provide shape as 2D matrix for rotation calculations

**Shape Definitions**:
- Each shape defined as list of (x, y) offsets from center
- Four rotation states pre-calculated for each shape type
- Colors assigned per shape type (I=cyan, O=yellow, T=purple, etc.)

### 2. Playfield (models/playfield.py)

**Purpose**: Manages the 10×20 grid state, tracking occupied cells and their colors.

**Key Attributes**:
- Width: Fixed at 10 columns
- Height: Fixed at 20 rows
- Grid: 2D array where each cell is either empty (None) or contains an RGB color

**Key Behaviors**:
- Validate position: Check if blocks fit without collision
- Add tetromino: Add stopped tetromino blocks to grid
- Get complete rows: Return indices of rows that are fully occupied
- Clear rows: Remove specified rows and shift remaining blocks down
- Check game over: Determine if any block exists in top row
- Get cell: Query color at specific position

### 3. GameState (models/game_state.py)

**Purpose**: Central game state manager coordinating all game logic and rules.

**Key Attributes**:
- Playfield: The 10×20 game grid
- Active tetromino: Currently falling piece (None if game over)
- Score: Current player score
- Game over flag: Whether the game has ended
- Fall timer: Time accumulator for automatic falling
- Fall interval: Time between automatic falls (e.g., 0.5 seconds)

**Key Behaviors**:
- Spawn tetromino: Create new random tetromino at top center
- Move active left/right: Attempt to move active tetromino horizontally
- Rotate active: Attempt to rotate active tetromino clockwise
- Hard drop: Drop active tetromino to bottom immediately
- Update: Handle automatic falling based on elapsed time
- Lock tetromino: Convert active to stopped, check lines, update score
- Can move: Validate if tetromino position is legal

**Game Logic Flow**:
1. Spawn tetromino at top center (x=4, y=0)
2. Process player input (move/rotate if valid)
3. Automatic fall: accumulate time, move down when interval reached
4. On landing: lock tetromino, check for complete rows, clear rows, update score, spawn next
5. Check game over condition after each lock

### 4. HighScoreManager (models/high_scores.py)

**Purpose**: Manage persistent high score storage and retrieval.

**Key Structures**:
- High score entry: Contains player name, score value, and timestamp
- Score list: Maintained in descending order, maximum 10 entries
- File path: Location of JSON persistence file (default: "high_scores.json")

**Key Behaviors**:
- Initialize and load: Read scores from JSON file on startup
- Save: Write scores to JSON file
- Add score: Add new score if it qualifies for top 10
- Check qualification: Determine if score belongs in top 10
- Get top scores: Retrieve top N scores

**JSON Storage Format**:
Scores stored as array of objects with name, score, and timestamp fields.

### 5. Renderer (views/renderer.py)

**Purpose**: Handle all Pygame-based graphics rendering.

**Configuration Constants**:
- Screen dimensions: 800×600 pixels
- Block size: 30 pixels per grid cell
- Playfield offset: Centered horizontally, 50 pixels from top
- Colors: Background (dark gray), grid lines (medium gray)

**Key Behaviors**:
- Render game: Draw complete game screen (playfield, tetromino, score)
- Render playfield: Draw grid and stopped blocks
- Render tetromino: Draw active falling piece
- Render score: Display score text
- Render grid lines: Draw playfield borders
- Clear screen: Fill with background color

**Rendering Order**:
1. Clear screen
2. Draw playfield grid lines
3. Draw stopped blocks from playfield
4. Draw active tetromino
5. Draw score and UI text
6. Update display

### 6. UIManager (views/ui_screens.py)

**Purpose**: Manage different game screens and transitions.

**Screen States**:
- START_SCREEN: Title and start prompt
- GAME_SCREEN: Active gameplay
- GAME_OVER_SCREEN: Final score display
- NAME_ENTRY_SCREEN: High score name input
- HIGH_SCORE_SCREEN: Top 10 display

**Key Behaviors**:
- Render start screen: Display title and "Press SPACE to start"
- Render game over screen: Display final score
- Render name entry screen: Show name input interface
- Render high scores: Display top 10 list
- Handle name entry input: Process text input events

### 7. InputHandler (controllers/input_handler.py)

**Purpose**: Process keyboard events and translate to game actions.

**Key Behaviors**:
- Handle game input: Process gameplay keyboard events
- Handle menu input: Process menu navigation
- Handle text input: Process text entry for names

**Input Mapping**:
- LEFT ARROW: Move active tetromino left
- RIGHT ARROW: Move active tetromino right
- SPACE: Rotate active tetromino clockwise
- DOWN ARROW: Hard drop
- ESCAPE: Pause/menu (optional)

## Data Models

### Tetromino Shape Configurations

Each tetromino type has four rotation states defined as lists of (x, y) block offsets from a center point. The shapes are:

- **I-Piece** (Cyan): 4 blocks in a line, rotates between horizontal and vertical orientations
- **O-Piece** (Yellow): 2×2 square, looks the same in all rotations
- **T-Piece** (Purple): T-shape, rotates to point in four directions (up, right, down, left)
- **L-Piece** (Orange): L-shape extending right, rotates through four orientations
- **J-Piece** (Dark Blue): L-shape extending left (mirror of L-piece), rotates through four orientations
- **S-Piece** (Green): Zigzag shape with offset to the right, rotates between horizontal and vertical
- **Z-Piece** (Red): Zigzag shape with offset to the left (mirror of S-piece), rotates between horizontal and vertical

Each shape's rotation states are pre-calculated and stored as constants to avoid runtime computation.

### Game State Transitions

```
START → SPAWNING → FALLING → (MOVING/ROTATING)* → LANDING → LINE_CHECK → SCORING → SPAWNING
                                                                    ↓
                                                              GAME_OVER
```

**State Invariants**:
- Playfield always 10×20
- Active tetromino always has exactly 4 blocks
- Score never decreases
- Complete rows always cleared before spawning next tetromino
- Game over only triggered when stopped blocks reach top row

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### What is Property-Based Testing?

Property-based testing is a testing methodology where instead of writing tests for specific hardcoded examples, you define general "properties" or "invariants" that should hold true for all valid inputs. The testing framework then automatically generates hundreds of random test cases to verify these properties.

**Traditional Example-Based Testing:**
```
Test: Adding a task to an empty list
- Start with empty list []
- Add task "Buy milk"
- Assert list length is 1
- Assert list contains "Buy milk"
```

**Property-Based Testing:**
```
Property: For ANY task and ANY list, adding the task increases the list length by 1
- Framework generates 100+ random combinations of tasks and lists
- Each combination is tested automatically
- If any combination fails, the framework reports the specific failing case
```

**Why Property-Based Testing for Tetris?**

Game logic is perfect for property-based testing because:
1. **Many possible states**: A Tetris game can be in millions of different states (different tetromino positions, playfield configurations, scores)
2. **Universal rules**: Rules like "tetrominoes can't move through walls" should work for ALL tetrominoes in ALL positions
3. **Edge case discovery**: Random generation finds corner cases you might not think of (e.g., rotating an L-piece in a tight space)
4. **Regression prevention**: Once a property passes, it continues to verify correctness as code changes

**How It Works in Practice:**

For example, Property 3 states: "For any tetromino and any playfield state, attempting to move beyond boundaries shall be prevented."

The Hypothesis library will:
- Generate random tetromino types (I, L, J, O, S, Z, T)
- Generate random positions (x, y coordinates)
- Generate random playfield states (with various stopped blocks)
- Try to move each tetromino beyond the left and right boundaries
- Verify that in ALL cases, the movement is prevented

If even ONE generated case fails, Hypothesis reports the exact failing combination, making it easy to fix the bug.

### Property Reflection

After analyzing all acceptance criteria, I've identified the following redundancies and consolidations:

**Redundancies to eliminate:**
- 3.5 and 3.6 are covered by 1.5 and 1.6 (boundary collision prevention)
- 3.10 is the same as 3.4 (hard drop behavior)
- 6.3 is covered by 6.2 (multiple row clearing scoring)
- 7.4 and 10.6 are duplicates (game over screen transition)
- 8.3 and 8.7 are covered by 8.2 (round-trip persistence)
- 9.1 and 10.8 are duplicates (name entry prompt)
- 2.9 is covered by individual shape tests (2.2-2.8)

**Properties to combine:**
- 1.5 and 1.6 can be combined into a single "boundary collision prevention" property
- 4.1 and 4.2 can be combined into a single "tetromino locking" property
- 6.1 and 6.2 can be combined into a comprehensive "scoring" property
- 7.2 and 7.3 can be combined into "game over state immutability" property

**Unique properties to keep:**
- Playfield dimensions (1.1)
- Playfield state tracking (1.4)
- Tetromino movement (3.1, 3.2, 3.3, 3.4)
- Collision detection (3.7, 3.8)
- Rotation center preservation (3.9)
- Line clearing mechanics (5.1-5.5)
- High score management (8.1, 8.4, 8.5, 8.6)
- High score persistence round-trip (8.2)

This reflection ensures each property provides unique validation value without logical redundancy.

### Correctness Properties

Based on the prework analysis and reflection, here are the correctness properties for property-based testing:

#### Property 1: Playfield Dimensions Invariant
*For any* Playfield instance, the grid dimensions shall always be exactly 10 columns and 20 rows.

**Validates: Requirements 1.1**

#### Property 2: Playfield State Accessibility
*For any* Playfield instance and any valid coordinates (x, y) where 0 ≤ x < 10 and 0 ≤ y < 20, querying the cell state shall return either None (empty) or a valid RGB color tuple.

**Validates: Requirements 1.4**

#### Property 3: Boundary Collision Prevention
*For any* tetromino and any playfield state, attempting to move the tetromino beyond the left boundary (x < 0) or right boundary (x + width > 10) shall be prevented, and the tetromino position shall remain unchanged.

**Validates: Requirements 1.5, 1.6, 3.5, 3.6**

#### Property 4: Tetromino Block Count Invariant
*For any* tetromino of any type and any rotation state, the tetromino shall always consist of exactly 4 blocks.

**Validates: Requirements 2.1-2.8**

#### Property 5: Movement Delta Correctness
*For any* tetromino at position (x, y), moving left shall result in position (x-1, y) if valid, moving right shall result in position (x+1, y) if valid, and the position shall remain unchanged if the move is invalid.

**Validates: Requirements 3.1, 3.2**

#### Property 6: Rotation Preserves Block Count
*For any* tetromino, rotating clockwise shall produce a new tetromino with exactly 4 blocks and the same color.

**Validates: Requirements 3.3**

#### Property 7: Hard Drop Reaches Bottom
*For any* tetromino and any playfield state, performing a hard drop shall move the tetromino to the lowest valid y-coordinate where it does not collide with the bottom or stopped blocks.

**Validates: Requirements 3.4, 3.10**

#### Property 8: Collision Detection Correctness
*For any* tetromino position and any playfield state with stopped blocks, attempting to move the tetromino into a position where any of its blocks would overlap with stopped blocks shall be prevented.

**Validates: Requirements 3.7**

#### Property 9: Rotation Collision Prevention
*For any* tetromino and any playfield state, attempting to rotate the tetromino into a configuration that would cause collision with boundaries or stopped blocks shall be prevented, and the tetromino shall remain in its current rotation state.

**Validates: Requirements 3.8**

#### Property 10: Rotation Center Preservation
*For any* tetromino at position (x, y), rotating the tetromino shall result in a new tetromino with the same center position (x, y).

**Validates: Requirements 3.9**

#### Property 11: Tetromino Locking Adds Blocks to Playfield
*For any* tetromino at a valid position, locking the tetromino shall result in the playfield containing blocks at each of the tetromino's absolute block positions with the tetromino's color.

**Validates: Requirements 4.1, 4.2, 4.3**

#### Property 12: Post-Lock Spawning
*For any* game state where a tetromino is locked (and game is not over), a new active tetromino shall be spawned at the top center position (x=4, y=0) with one of the seven valid tetromino types.

**Validates: Requirements 4.4, 4.5**

#### Property 13: Complete Row Detection
*For any* playfield state, a row at index y is complete if and only if all 10 positions in that row contain non-None color values.

**Validates: Requirements 5.1**

#### Property 14: Row Clearing Empties Rows
*For any* playfield state with complete rows, clearing those rows shall result in those row indices containing only None values (empty cells).

**Validates: Requirements 5.2**

#### Property 15: Row Clearing Gravity
*For any* playfield state where row y is cleared, all blocks in rows above y (rows 0 to y-1) shall move down by one row, preserving their colors and relative positions.

**Validates: Requirements 5.3, 5.5**

#### Property 16: Multiple Row Clearing
*For any* playfield state with N complete rows, clearing all complete rows shall remove exactly N rows and shift all rows above the highest cleared row down by N positions.

**Validates: Requirements 5.4**

#### Property 17: Scoring Monotonicity
*For any* game state and any sequence of valid game actions, the score shall never decrease.

**Validates: Requirements 6.4**

#### Property 18: Tetromino Lock Scoring
*For any* game state with score S, locking a tetromino (without clearing rows) shall result in score S + 4.

**Validates: Requirements 6.1**

#### Property 19: Line Clear Scoring
*For any* game state with score S, clearing N complete rows shall increase the score by N × 10 points (in addition to the 4 points for locking the tetromino).

**Validates: Requirements 6.2, 6.3**

#### Property 20: Game Over Detection
*For any* playfield state, the game is over if and only if any stopped block exists at row index 0 (the top row).

**Validates: Requirements 7.1**

#### Property 21: Game Over State Immutability
*For any* game state where game over is true, no game actions (move, rotate, spawn) shall modify the playfield or active tetromino state.

**Validates: Requirements 7.2, 7.3**

#### Property 22: High Score List Size Limit
*For any* high score manager state, the high score list shall contain at most 10 entries.

**Validates: Requirements 8.1**

#### Property 23: High Score Persistence Round-Trip
*For any* valid high score list, saving the list to JSON and then loading it shall produce an equivalent list with the same scores, names, and order.

**Validates: Requirements 8.2, 8.3, 8.7, 9.4**

#### Property 24: High Score Qualification
*For any* high score list and any score value, the score qualifies for the top 10 if and only if the list has fewer than 10 entries OR the score is greater than the lowest score in the list.

**Validates: Requirements 8.4**

#### Property 25: High Score Addition
*For any* high score list and any qualifying score with name, adding the score shall result in a list that contains the new entry and maintains at most 10 entries.

**Validates: Requirements 8.5**

#### Property 26: High Score Sorting Invariant
*For any* high score list after any add operation, the list shall be sorted in descending order by score value.

**Validates: Requirements 8.6**

#### Property 27: High Score Entry Completeness
*For any* high score entry in the list, the entry shall contain both a non-empty name string and a non-negative integer score value.

**Validates: Requirements 9.3**

## Error Handling

### Input Validation
- **Invalid tetromino types**: Attempting to create a tetromino with an invalid type string shall raise a `ValueError`
- **Out-of-bounds coordinates**: Querying playfield cells with invalid coordinates shall raise an `IndexError`
- **Invalid rotation values**: Rotation state must be 0, 1, 2, or 3; other values shall raise a `ValueError`

### File System Errors
- **Missing high score file**: If the JSON file doesn't exist on load, create an empty file with an empty score list
- **Corrupted JSON**: If the JSON file is malformed, log a warning and initialize with an empty score list
- **Write permission errors**: If unable to write to the high score file, log an error but allow gameplay to continue

### Game State Errors
- **Spawn collision**: If a new tetromino cannot be spawned at the top center without collision, trigger game over immediately
- **Invalid game state**: If the playfield or game state becomes corrupted, log the error and reset to a new game

### Pygame Errors
- **Display initialization failure**: If Pygame cannot initialize the display, exit gracefully with an error message
- **Font loading failure**: If fonts cannot be loaded, fall back to Pygame's default font
- **Event processing errors**: Catch and log any unexpected Pygame event errors to prevent crashes

## Testing Strategy

### Dual Testing Approach

This project employs both unit testing and property-based testing to ensure comprehensive correctness:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Test each of the seven tetromino shapes with their exact configurations
- Test specific game scenarios (e.g., clearing a single row, game over at spawn)
- Test edge cases (empty playfield, full playfield, boundary conditions)
- Test error handling (invalid inputs, file system errors)
- Test UI state transitions (start → game → game over)

**Property Tests**: Verify universal properties across all inputs
- Use the [Hypothesis library](https://hypothesis.readthedocs.io/) for property-based testing
- Each property test shall run a minimum of 100 iterations to ensure comprehensive coverage
- Each property test shall be tagged with a comment referencing its design property
- Tag format: `# Feature: tetris-clone, Property N: [property title]`

### Property-Based Testing Configuration

**Library**: Hypothesis (Python property-based testing library)

**Test Configuration**:
```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)
@given(...)
def test_property_name(...):
    # Feature: tetris-clone, Property N: [property title]
    # Test implementation
    pass
```

**Custom Strategies**:
- `tetromino_type()`: Generate random tetromino types ('I', 'L', 'J', 'O', 'S', 'Z', 'T')
- `position()`: Generate random valid positions (x: 0-9, y: 0-19)
- `playfield_state()`: Generate random playfield configurations
- `game_state()`: Generate random valid game states
- `high_score_list()`: Generate random high score lists

### Test Coverage Goals

- **Core game logic**: 100% coverage of game state, playfield, and tetromino classes
- **Collision detection**: All boundary and block collision scenarios
- **Line clearing**: All combinations of single and multiple row clears
- **Scoring**: All scoring scenarios (lock, single line, multiple lines)
- **High scores**: All persistence and ranking scenarios
- **Error handling**: All error conditions and edge cases

### Testing Isolation

- **No Pygame dependencies in core tests**: Core game logic tests shall not require Pygame initialization
- **Mock rendering**: Renderer tests shall use mock surfaces to avoid display requirements
- **Temporary files**: High score persistence tests shall use temporary files that are cleaned up after tests
- **Deterministic randomness**: Use seeded random number generators for reproducible tests

### Integration Testing

While property-based tests cover the core logic comprehensively, integration tests verify:
- Game loop timing and frame rate consistency
- Input handler integration with game state
- Renderer integration with game state
- UI screen transitions
- End-to-end gameplay scenarios

### Test Organization

```
tests/
├── test_tetromino.py          # Tetromino shape, rotation, movement properties
├── test_playfield.py          # Playfield state, collision, line clearing properties
├── test_game_state.py         # Game state, scoring, game over properties
├── test_high_scores.py        # High score persistence and ranking properties
├── test_renderer.py           # Rendering unit tests (with mocks)
├── test_input_handler.py      # Input handling unit tests
├── test_ui_manager.py         # UI state transition unit tests
└── test_integration.py        # End-to-end integration tests
```

Each test file shall contain both unit tests (for specific examples) and property tests (for universal properties), clearly separated and documented.

