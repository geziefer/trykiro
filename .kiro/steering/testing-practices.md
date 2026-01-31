---
inclusion: always
---

# Testing Practices

## Overview

This document defines comprehensive testing practices for the Tetris clone project. We use a dual testing approach: unit tests for specific examples and property-based tests for universal correctness properties.

## Testing Philosophy

### Core Principles
1. **Tests are documentation** - They show how the code should be used
2. **Tests verify correctness** - They prove the code meets requirements
3. **Tests enable refactoring** - They catch regressions when changing code
4. **Tests should be fast** - Run the full suite in seconds, not minutes

### What to Test
- **Core game logic**: 100% coverage of models/ (GameState, Playfield, Tetromino)
- **Business rules**: All scoring, collision, line clearing logic
- **Edge cases**: Boundary conditions, empty states, full states
- **Error handling**: Invalid inputs, file system errors
- **Integration points**: How components work together

### What NOT to Test
- Pygame rendering details (mock the surfaces instead)
- Third-party library internals (trust pygame, hypothesis)
- Trivial getters/setters (unless they have logic)

## Test Organization

### Directory Structure
```
tests/
├── __init__.py
├── test_tetromino.py          # Tetromino unit + property tests
├── test_playfield.py          # Playfield unit + property tests
├── test_game_state.py         # GameState unit + property tests
├── test_high_scores.py        # High score unit + property tests
├── test_renderer.py           # Renderer unit tests (with mocks)
├── test_input_handler.py      # Input handler unit tests
├── test_ui_manager.py         # UI manager unit tests
├── test_integration.py        # End-to-end integration tests
└── strategies.py              # Hypothesis custom strategies
```

### File Naming
- Test files: `test_<module_name>.py`
- Test functions: `test_<what_is_being_tested>`
- Property tests: `test_property_<property_number>_<brief_name>`

## Unit Testing

### Framework
- Use **pytest** as the test runner
- Use pytest fixtures for common setup
- Use pytest parametrize for multiple similar test cases

### Unit Test Structure
Follow the Arrange-Act-Assert pattern:
```python
def test_tetromino_move_left():
    # Arrange - Set up test data
    tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
    
    # Act - Perform the operation
    moved = tetromino.move(-1, 0)
    
    # Assert - Verify the result
    assert moved.x == 4
    assert moved.y == 10
    assert moved.shape_type == 'I'
```

### Test Naming
Test names should describe the scenario and expected outcome:
- `test_spawn_tetromino_returns_random_type`
- `test_move_left_at_boundary_prevents_movement`
- `test_clear_multiple_rows_shifts_blocks_correctly`
- `test_game_over_when_block_in_top_row`

### Fixtures
Use fixtures for common test setup:
```python
import pytest
from models.playfield import Playfield
from models.game_state import GameState

@pytest.fixture
def empty_playfield():
    """Provide a fresh empty playfield."""
    return Playfield()

@pytest.fixture
def game_state():
    """Provide a fresh game state."""
    return GameState()

@pytest.fixture
def playfield_with_bottom_row():
    """Provide a playfield with bottom row almost complete."""
    playfield = Playfield()
    for x in range(9):  # Fill 9 of 10 positions
        playfield.set_cell(x, 19, (255, 0, 0))
    return playfield
```

### Parametrized Tests
Use parametrize for testing multiple similar cases:
```python
@pytest.mark.parametrize("shape_type,expected_color", [
    ('I', (0, 255, 255)),      # Cyan
    ('O', (255, 255, 0)),      # Yellow
    ('T', (128, 0, 128)),      # Purple
    ('L', (255, 165, 0)),      # Orange
    ('J', (0, 0, 255)),        # Dark blue
    ('S', (0, 255, 0)),        # Green
    ('Z', (255, 0, 0)),        # Red
])
def test_tetromino_colors(shape_type, expected_color):
    tetromino = Tetromino(shape_type=shape_type, x=0, y=0, rotation=0)
    assert tetromino.color == expected_color
```

## Property-Based Testing

### Framework
- Use **Hypothesis** for property-based testing
- Configure with `@settings(max_examples=100)` for thorough coverage
- Define custom strategies in `tests/strategies.py`

### Property Test Structure
```python
from hypothesis import given, settings, strategies as st
from tests.strategies import tetromino_type, valid_position

@settings(max_examples=100)
@given(
    shape_type=tetromino_type(),
    rotation=st.integers(min_value=0, max_value=3)
)
def test_property_4_tetromino_block_count_invariant(shape_type, rotation):
    """Property 4: Any tetromino always has exactly 4 blocks.
    
    Feature: tetris-clone, Property 4: Tetromino Block Count Invariant
    Validates: Requirements 2.1-2.8
    """
    tetromino = Tetromino(shape_type=shape_type, x=0, y=0, rotation=rotation)
    blocks = tetromino.get_absolute_blocks()
    assert len(blocks) == 4, f"Tetromino {shape_type} has {len(blocks)} blocks, expected 4"
```

### Property Test Naming and Documentation
- Function name: `test_property_<N>_<brief_description>`
- Docstring MUST include:
  - Property number and title
  - Feature reference
  - Requirements validated
- Tag format: `# Feature: tetris-clone, Property N: [title]`

### Custom Strategies
Define reusable strategies in `tests/strategies.py`:
```python
from hypothesis import strategies as st
from models.tetromino import Tetromino
from models.playfield import Playfield

def tetromino_type():
    """Strategy for generating valid tetromino types."""
    return st.sampled_from(['I', 'O', 'T', 'L', 'J', 'S', 'Z'])

def valid_position():
    """Strategy for generating valid playfield positions."""
    return st.tuples(
        st.integers(min_value=0, max_value=9),   # x
        st.integers(min_value=0, max_value=19)   # y
    )

def tetromino():
    """Strategy for generating random tetrominoes."""
    return st.builds(
        Tetromino,
        shape_type=tetromino_type(),
        x=st.integers(min_value=-2, max_value=11),
        y=st.integers(min_value=-2, max_value=21),
        rotation=st.integers(min_value=0, max_value=3)
    )

@st.composite
def playfield_with_blocks(draw):
    """Strategy for generating playfields with random stopped blocks."""
    playfield = Playfield()
    num_blocks = draw(st.integers(min_value=0, max_value=50))
    for _ in range(num_blocks):
        x = draw(st.integers(min_value=0, max_value=9))
        y = draw(st.integers(min_value=0, max_value=19))
        color = draw(st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255)
        ))
        playfield.set_cell(x, y, color)
    return playfield
```

### Property Test Best Practices
- **Keep properties simple** - Test one invariant per property
- **Use descriptive assertions** - Include helpful error messages
- **Shrink effectively** - Hypothesis will find minimal failing cases
- **Assume valid inputs** - Use `hypothesis.assume()` to filter invalid cases
- **Deterministic tests** - Don't rely on global state

### Example with Assumptions
```python
@settings(max_examples=100)
@given(
    tetromino=tetromino(),
    playfield=playfield_with_blocks()
)
def test_property_8_collision_detection(tetromino, playfield):
    """Property 8: Moving into occupied space is prevented.
    
    Feature: tetris-clone, Property 8: Collision Detection Correctness
    Validates: Requirements 3.7
    """
    # Only test if tetromino is currently in valid position
    assume(playfield.is_valid_position(tetromino))
    
    # Try to move into each direction
    for dx, dy in [(-1, 0), (1, 0), (0, 1)]:
        moved = tetromino.move(dx, dy)
        if not playfield.is_valid_position(moved):
            # Movement should be prevented by game state
            assert not game_state.can_move(tetromino, dx, dy)
```

## Test Isolation

### No Side Effects
- Tests must not depend on execution order
- Each test should set up its own data
- Clean up any files created during tests

### Temporary Files
For high score persistence tests:
```python
import tempfile
import os
import pytest

@pytest.fixture
def temp_high_score_file():
    """Provide a temporary file for high score testing."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.remove(path)

def test_high_score_persistence(temp_high_score_file):
    manager = HighScoreManager(file_path=temp_high_score_file)
    manager.add_score("Alice", 1000)
    manager.save()
    
    # Load in new instance
    manager2 = HighScoreManager(file_path=temp_high_score_file)
    manager2.load()
    assert len(manager2.scores) == 1
    assert manager2.scores[0].name == "Alice"
```

### Mocking Pygame
For renderer tests, mock Pygame surfaces:
```python
from unittest.mock import Mock, MagicMock
import pytest

@pytest.fixture
def mock_pygame_surface():
    """Provide a mock Pygame surface."""
    surface = MagicMock()
    surface.fill = Mock()
    surface.blit = Mock()
    return surface

def test_renderer_draws_tetromino(mock_pygame_surface):
    renderer = Renderer(surface=mock_pygame_surface)
    tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
    
    renderer.render_tetromino(tetromino)
    
    # Verify drawing methods were called
    assert mock_pygame_surface.fill.called or mock_pygame_surface.blit.called
```

## Test Coverage

### Coverage Goals
- **Core logic (models/)**: 100% line coverage
- **Views and controllers**: 80%+ coverage
- **Overall project**: 90%+ coverage

### Running Coverage
```bash
pytest --cov=tetris --cov-report=html --cov-report=term
```

### Coverage Exclusions
Exclude from coverage:
- `if __name__ == '__main__':` blocks
- Defensive assertions that should never trigger
- Pygame initialization code (hard to test)

## Integration Testing

### Purpose
Integration tests verify that components work together correctly:
- Game loop timing
- Input → GameState → Renderer flow
- UI state transitions
- End-to-end gameplay scenarios

### Integration Test Example
```python
def test_complete_game_flow():
    """Test a complete game from start to game over."""
    game_state = GameState()
    
    # Spawn initial tetromino
    game_state.spawn_tetromino()
    assert game_state.active_tetromino is not None
    
    # Play until game over
    moves = 0
    while not game_state.game_over and moves < 1000:
        # Simulate random moves
        game_state.move_active_left()
        game_state.update(0.1)  # Simulate time passing
        moves += 1
    
    # Verify game ended properly
    assert game_state.game_over or moves == 1000
    assert game_state.score >= 0
```

## Test Execution

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tetromino.py

# Run specific test
pytest tests/test_tetromino.py::test_tetromino_move_left

# Run only property tests
pytest -k "property"

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=tetris
```

### Continuous Testing
- Run tests before every commit
- Run full test suite before pushing
- Consider using pytest-watch for automatic re-running

## Debugging Failed Tests

### Hypothesis Failures
When a property test fails, Hypothesis provides:
- The minimal failing example
- The exact inputs that caused failure
- A seed to reproduce the failure

Example output:
```
Falsifying example: test_property_3_boundary_collision(
    tetromino=Tetromino(shape_type='I', x=9, y=5, rotation=1)
)
```

### Debugging Strategy
1. Read the failure message carefully
2. Reproduce with the exact inputs provided
3. Add print statements or use debugger
4. Fix the bug
5. Verify the property test passes
6. Run full suite to check for regressions

## Test Quality Checklist

Before considering tests complete:
- [ ] All 27 properties have property tests
- [ ] Each property test runs 100+ examples
- [ ] Property tests are properly tagged and documented
- [ ] Unit tests cover edge cases and error conditions
- [ ] Tests are isolated (no shared state)
- [ ] Tests are fast (full suite under 10 seconds)
- [ ] Coverage meets goals (90%+ overall)
- [ ] No flaky tests (tests pass consistently)
- [ ] Test names are descriptive
- [ ] Mocks are used appropriately (not overused)
