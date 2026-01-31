"""Unit and property-based tests for the Playfield class.

This module contains tests for the Playfield class, including:
- Unit tests for specific examples and edge cases
- Property-based tests for universal correctness properties
"""

import pytest
from hypothesis import given, settings, strategies as st

from tetris.models.playfield import Playfield, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT


# ============================================================================
# Unit Tests
# ============================================================================

def test_playfield_initialization():
    """Test that a new playfield is initialized with correct dimensions."""
    playfield = Playfield()
    
    assert playfield.width == PLAYFIELD_WIDTH
    assert playfield.height == PLAYFIELD_HEIGHT
    assert playfield.width == 10
    assert playfield.height == 20


def test_playfield_initially_empty():
    """Test that all cells in a new playfield are empty (None)."""
    playfield = Playfield()
    
    for y in range(playfield.height):
        for x in range(playfield.width):
            assert playfield.get_cell(x, y) is None


def test_set_and_get_cell():
    """Test setting and getting cell values."""
    playfield = Playfield()
    color = (255, 0, 0)  # Red
    
    # Set a cell
    playfield.set_cell(5, 10, color)
    
    # Verify it was set
    assert playfield.get_cell(5, 10) == color
    
    # Verify other cells are still empty
    assert playfield.get_cell(4, 10) is None
    assert playfield.get_cell(6, 10) is None
    assert playfield.get_cell(5, 9) is None
    assert playfield.get_cell(5, 11) is None


def test_set_cell_to_none_clears_cell():
    """Test that setting a cell to None clears it."""
    playfield = Playfield()
    color = (0, 255, 0)  # Green
    
    # Set a cell
    playfield.set_cell(3, 7, color)
    assert playfield.get_cell(3, 7) == color
    
    # Clear the cell
    playfield.set_cell(3, 7, None)
    assert playfield.get_cell(3, 7) is None


def test_get_cell_out_of_bounds_raises_error():
    """Test that accessing out-of-bounds cells raises IndexError."""
    playfield = Playfield()
    
    # Test x out of bounds
    with pytest.raises(IndexError):
        playfield.get_cell(-1, 5)
    
    with pytest.raises(IndexError):
        playfield.get_cell(10, 5)
    
    # Test y out of bounds
    with pytest.raises(IndexError):
        playfield.get_cell(5, -1)
    
    with pytest.raises(IndexError):
        playfield.get_cell(5, 20)


def test_set_cell_out_of_bounds_raises_error():
    """Test that setting out-of-bounds cells raises IndexError."""
    playfield = Playfield()
    color = (0, 0, 255)  # Blue
    
    # Test x out of bounds
    with pytest.raises(IndexError):
        playfield.set_cell(-1, 5, color)
    
    with pytest.raises(IndexError):
        playfield.set_cell(10, 5, color)
    
    # Test y out of bounds
    with pytest.raises(IndexError):
        playfield.set_cell(5, -1, color)
    
    with pytest.raises(IndexError):
        playfield.set_cell(5, 20, color)


def test_boundary_cells_accessible():
    """Test that all boundary cells are accessible."""
    playfield = Playfield()
    color = (128, 128, 128)  # Gray
    
    # Test corners
    playfield.set_cell(0, 0, color)
    assert playfield.get_cell(0, 0) == color
    
    playfield.set_cell(9, 0, color)
    assert playfield.get_cell(9, 0) == color
    
    playfield.set_cell(0, 19, color)
    assert playfield.get_cell(0, 19) == color
    
    playfield.set_cell(9, 19, color)
    assert playfield.get_cell(9, 19) == color


def test_is_valid_position_empty_playfield():
    """Test that tetrominoes in valid positions are accepted on empty playfield."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Tetromino in the middle should be valid
    tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is True
    
    # Tetromino at top center (spawn position) should be valid
    tetromino = Tetromino(shape_type='T', x=4, y=0, rotation=0)
    assert playfield.is_valid_position(tetromino) is True


def test_is_valid_position_left_boundary():
    """Test that tetrominoes beyond left boundary are rejected."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # I-piece horizontal at x=-1 should be invalid (blocks at -1, 0, 1, 2)
    tetromino = Tetromino(shape_type='I', x=-1, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is False
    
    # O-piece at x=-1 should be invalid (blocks at -1, 0)
    tetromino = Tetromino(shape_type='O', x=-1, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is False


def test_is_valid_position_right_boundary():
    """Test that tetrominoes beyond right boundary are rejected."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # I-piece horizontal at x=7 should be invalid (blocks at 7, 8, 9, 10)
    tetromino = Tetromino(shape_type='I', x=7, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is False
    
    # O-piece at x=9 should be invalid (blocks at 9, 10)
    tetromino = Tetromino(shape_type='O', x=9, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is False


def test_is_valid_position_top_boundary():
    """Test that tetrominoes above top boundary are rejected."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Tetromino with blocks above y=0 should be invalid
    tetromino = Tetromino(shape_type='I', x=5, y=-1, rotation=1)  # Vertical I-piece
    assert playfield.is_valid_position(tetromino) is False


def test_is_valid_position_bottom_boundary():
    """Test that tetrominoes below bottom boundary are rejected."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # I-piece vertical at y=17 should be invalid (blocks at 17, 18, 19, 20)
    tetromino = Tetromino(shape_type='I', x=5, y=17, rotation=1)
    assert playfield.is_valid_position(tetromino) is False
    
    # O-piece at y=19 should be invalid (blocks at 19, 20)
    tetromino = Tetromino(shape_type='O', x=5, y=19, rotation=0)
    assert playfield.is_valid_position(tetromino) is False


def test_is_valid_position_collision_with_stopped_blocks():
    """Test that tetrominoes colliding with stopped blocks are rejected."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Place some stopped blocks
    playfield.set_cell(5, 10, (255, 0, 0))
    playfield.set_cell(6, 10, (255, 0, 0))
    
    # Tetromino overlapping with stopped blocks should be invalid
    tetromino = Tetromino(shape_type='I', x=4, y=10, rotation=0)  # Blocks at 4, 5, 6, 7
    assert playfield.is_valid_position(tetromino) is False
    
    # Tetromino not overlapping should be valid
    tetromino = Tetromino(shape_type='I', x=1, y=10, rotation=0)  # Blocks at 1, 2, 3, 4
    assert playfield.is_valid_position(tetromino) is True


def test_is_valid_position_at_boundaries_valid():
    """Test that tetrominoes exactly at boundaries (but not beyond) are valid."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # I-piece horizontal at x=0 should be valid (blocks at 0, 1, 2, 3)
    tetromino = Tetromino(shape_type='I', x=0, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is True
    
    # I-piece horizontal at x=6 should be valid (blocks at 6, 7, 8, 9)
    tetromino = Tetromino(shape_type='I', x=6, y=10, rotation=0)
    assert playfield.is_valid_position(tetromino) is True
    
    # I-piece vertical at y=16 should be valid (blocks at 16, 17, 18, 19)
    tetromino = Tetromino(shape_type='I', x=5, y=16, rotation=1)
    assert playfield.is_valid_position(tetromino) is True


def test_is_valid_position_complex_collision():
    """Test collision detection with complex playfield state."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Create a complex pattern of stopped blocks
    for x in range(0, 5):
        playfield.set_cell(x, 18, (255, 0, 0))
    for x in range(5, 10):
        playfield.set_cell(x, 19, (0, 255, 0))
    
    # T-piece at y=17 should be valid (above the stopped blocks)
    tetromino = Tetromino(shape_type='T', x=5, y=16, rotation=0)
    assert playfield.is_valid_position(tetromino) is True
    
    # T-piece at y=18 should be invalid (collides with stopped blocks)
    tetromino = Tetromino(shape_type='T', x=2, y=17, rotation=0)
    assert playfield.is_valid_position(tetromino) is False


def test_add_tetromino_basic():
    """Test that add_tetromino locks blocks into the grid with correct colors."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Create an I-piece (cyan) at position (5, 10) horizontal
    tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
    cyan = (0, 255, 255)
    
    # Verify playfield is empty at those positions
    assert playfield.get_cell(5, 10) is None
    assert playfield.get_cell(6, 10) is None
    assert playfield.get_cell(7, 10) is None
    assert playfield.get_cell(8, 10) is None
    
    # Add the tetromino
    playfield.add_tetromino(tetromino)
    
    # Verify blocks are now in the grid with correct color
    assert playfield.get_cell(5, 10) == cyan
    assert playfield.get_cell(6, 10) == cyan
    assert playfield.get_cell(7, 10) == cyan
    assert playfield.get_cell(8, 10) == cyan
    
    # Verify adjacent cells are still empty
    assert playfield.get_cell(4, 10) is None
    assert playfield.get_cell(9, 10) is None
    assert playfield.get_cell(5, 9) is None
    assert playfield.get_cell(5, 11) is None


def test_add_tetromino_different_shapes():
    """Test add_tetromino with different tetromino shapes."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Add an O-piece (yellow) at (2, 5)
    o_piece = Tetromino(shape_type='O', x=2, y=5, rotation=0)
    yellow = (255, 255, 0)
    playfield.add_tetromino(o_piece)
    
    # Verify O-piece blocks (2x2 square at positions 2,3 x 5,6)
    assert playfield.get_cell(2, 5) == yellow
    assert playfield.get_cell(3, 5) == yellow
    assert playfield.get_cell(2, 6) == yellow
    assert playfield.get_cell(3, 6) == yellow
    
    # Add a T-piece (purple) at (6, 8)
    t_piece = Tetromino(shape_type='T', x=6, y=8, rotation=0)
    purple = (128, 0, 128)
    playfield.add_tetromino(t_piece)
    
    # Verify T-piece blocks (T pointing up: [(1,0), (0,1), (1,1), (2,1)])
    # At position (6,8): blocks are at (7,8), (6,9), (7,9), (8,9)
    assert playfield.get_cell(7, 8) == purple  # Top center
    assert playfield.get_cell(6, 9) == purple  # Bottom left
    assert playfield.get_cell(7, 9) == purple  # Bottom center
    assert playfield.get_cell(8, 9) == purple  # Bottom right
    
    # Verify O-piece blocks are still there
    assert playfield.get_cell(2, 5) == yellow
    assert playfield.get_cell(3, 5) == yellow


def test_add_tetromino_multiple_pieces():
    """Test adding multiple tetrominoes to build up the playfield."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Add I-piece at (1, 16) horizontal: blocks at (1,16), (2,16), (3,16), (4,16)
    i_piece = Tetromino(shape_type='I', x=1, y=16, rotation=0)
    cyan = (0, 255, 255)
    playfield.add_tetromino(i_piece)
    
    # Verify I-piece blocks
    assert playfield.get_cell(1, 16) == cyan
    assert playfield.get_cell(2, 16) == cyan
    assert playfield.get_cell(3, 16) == cyan
    assert playfield.get_cell(4, 16) == cyan
    
    # Add L-piece at (5, 17): blocks at (7,17), (5,18), (6,18), (7,18)
    l_piece = Tetromino(shape_type='L', x=5, y=17, rotation=0)
    orange = (255, 165, 0)
    playfield.add_tetromino(l_piece)
    
    # Verify L-piece blocks
    assert playfield.get_cell(7, 17) == orange
    assert playfield.get_cell(5, 18) == orange
    assert playfield.get_cell(6, 18) == orange
    assert playfield.get_cell(7, 18) == orange
    
    # Verify I-piece blocks are still there
    assert playfield.get_cell(1, 16) == cyan
    assert playfield.get_cell(2, 16) == cyan


def test_add_tetromino_at_boundaries():
    """Test add_tetromino works correctly at playfield boundaries."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Add I-piece at left boundary (horizontal)
    left_piece = Tetromino(shape_type='I', x=0, y=0, rotation=0)
    cyan = (0, 255, 255)
    playfield.add_tetromino(left_piece)
    
    assert playfield.get_cell(0, 0) == cyan
    assert playfield.get_cell(1, 0) == cyan
    assert playfield.get_cell(2, 0) == cyan
    assert playfield.get_cell(3, 0) == cyan
    
    # Add I-piece at right boundary (horizontal)
    right_piece = Tetromino(shape_type='I', x=6, y=1, rotation=0)
    playfield.add_tetromino(right_piece)
    
    assert playfield.get_cell(6, 1) == cyan
    assert playfield.get_cell(7, 1) == cyan
    assert playfield.get_cell(8, 1) == cyan
    assert playfield.get_cell(9, 1) == cyan
    
    # Add I-piece at bottom boundary (vertical)
    # I-piece vertical rotation 1: blocks at [(1,0), (1,1), (1,2), (1,3)]
    # At position (5, 16): blocks are at (6,16), (6,17), (6,18), (6,19)
    bottom_piece = Tetromino(shape_type='I', x=5, y=16, rotation=1)
    playfield.add_tetromino(bottom_piece)
    
    assert playfield.get_cell(6, 16) == cyan
    assert playfield.get_cell(6, 17) == cyan
    assert playfield.get_cell(6, 18) == cyan
    assert playfield.get_cell(6, 19) == cyan


def test_add_tetromino_with_rotation():
    """Test add_tetromino with different rotation states."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Add I-piece horizontal (rotation 0)
    h_piece = Tetromino(shape_type='I', x=1, y=5, rotation=0)
    cyan = (0, 255, 255)
    playfield.add_tetromino(h_piece)
    
    # Verify horizontal placement
    assert playfield.get_cell(1, 5) == cyan
    assert playfield.get_cell(2, 5) == cyan
    assert playfield.get_cell(3, 5) == cyan
    assert playfield.get_cell(4, 5) == cyan
    
    # Add I-piece vertical (rotation 1)
    # I-piece vertical rotation 1: blocks at [(1,0), (1,1), (1,2), (1,3)]
    # At position (7, 10): blocks are at (8,10), (8,11), (8,12), (8,13)
    v_piece = Tetromino(shape_type='I', x=7, y=10, rotation=1)
    playfield.add_tetromino(v_piece)
    
    # Verify vertical placement
    assert playfield.get_cell(8, 10) == cyan
    assert playfield.get_cell(8, 11) == cyan
    assert playfield.get_cell(8, 12) == cyan
    assert playfield.get_cell(8, 13) == cyan


def test_get_complete_rows_empty_playfield():
    """Test that get_complete_rows returns empty list for empty playfield."""
    playfield = Playfield()
    
    complete_rows = playfield.get_complete_rows()
    
    assert complete_rows == []


def test_get_complete_rows_no_complete_rows():
    """Test that get_complete_rows returns empty list when no rows are complete."""
    playfield = Playfield()
    
    # Fill some cells but not complete rows
    for x in range(5):
        playfield.set_cell(x, 19, (255, 0, 0))
    
    for x in range(3, 8):
        playfield.set_cell(x, 18, (0, 255, 0))
    
    complete_rows = playfield.get_complete_rows()
    
    assert complete_rows == []


def test_get_complete_rows_single_complete_row():
    """Test that get_complete_rows detects a single complete row."""
    playfield = Playfield()
    
    # Fill the bottom row completely
    for x in range(10):
        playfield.set_cell(x, 19, (255, 0, 0))
    
    complete_rows = playfield.get_complete_rows()
    
    assert complete_rows == [19]


def test_get_complete_rows_multiple_complete_rows():
    """Test that get_complete_rows detects multiple complete rows."""
    playfield = Playfield()
    
    # Fill rows 17, 18, and 19 completely
    for y in [17, 18, 19]:
        for x in range(10):
            playfield.set_cell(x, y, (0, 255, 0))
    
    complete_rows = playfield.get_complete_rows()
    
    assert complete_rows == [17, 18, 19]


def test_get_complete_rows_non_consecutive():
    """Test that get_complete_rows detects non-consecutive complete rows."""
    playfield = Playfield()
    
    # Fill rows 15 and 19 completely, but not rows in between
    for x in range(10):
        playfield.set_cell(x, 15, (255, 0, 0))
        playfield.set_cell(x, 19, (0, 0, 255))
    
    # Fill row 17 partially (not complete)
    for x in range(7):
        playfield.set_cell(x, 17, (0, 255, 0))
    
    complete_rows = playfield.get_complete_rows()
    
    assert complete_rows == [15, 19]


def test_get_complete_rows_top_row():
    """Test that get_complete_rows can detect complete row at top."""
    playfield = Playfield()
    
    # Fill the top row completely
    for x in range(10):
        playfield.set_cell(x, 0, (128, 128, 128))
    
    complete_rows = playfield.get_complete_rows()
    
    assert complete_rows == [0]


def test_clear_rows_empty_list():
    """Test that clear_rows with empty list does nothing."""
    playfield = Playfield()
    
    # Fill some cells
    playfield.set_cell(5, 10, (255, 0, 0))
    playfield.set_cell(3, 15, (0, 255, 0))
    
    # Clear no rows
    playfield.clear_rows([])
    
    # Verify cells are unchanged
    assert playfield.get_cell(5, 10) == (255, 0, 0)
    assert playfield.get_cell(3, 15) == (0, 255, 0)


def test_clear_rows_single_row():
    """Test clearing a single complete row."""
    playfield = Playfield()
    
    # Fill bottom row
    for x in range(10):
        playfield.set_cell(x, 19, (255, 0, 0))
    
    # Place a block above it
    playfield.set_cell(5, 18, (0, 255, 0))
    
    # Clear the bottom row
    playfield.clear_rows([19])
    
    # Block that was at row 18 should now be at row 19
    assert playfield.get_cell(5, 19) == (0, 255, 0)
    assert playfield.get_cell(5, 18) is None
    
    # Other cells in row 19 should be empty (they were empty in row 18)
    for x in range(10):
        if x != 5:
            assert playfield.get_cell(x, 19) is None


def test_clear_rows_multiple_consecutive_rows():
    """Test clearing multiple consecutive rows."""
    playfield = Playfield()
    
    # Fill rows 18 and 19
    for y in [18, 19]:
        for x in range(10):
            playfield.set_cell(x, y, (255, 0, 0))
    
    # Place blocks above
    playfield.set_cell(3, 17, (0, 255, 0))
    playfield.set_cell(7, 16, (0, 0, 255))
    
    # Clear rows 18 and 19
    playfield.clear_rows([18, 19])
    
    # Blocks should have shifted down by 2
    assert playfield.get_cell(3, 19) == (0, 255, 0)  # Was at 17, now at 19
    assert playfield.get_cell(7, 18) == (0, 0, 255)  # Was at 16, now at 18
    
    # Original positions should be empty
    assert playfield.get_cell(3, 17) is None
    assert playfield.get_cell(7, 16) is None
    
    # Other cells in rows 18 and 19 should be empty (they were empty above)
    for x in range(10):
        if x != 7:
            assert playfield.get_cell(x, 18) is None
        if x != 3:
            assert playfield.get_cell(x, 19) is None


def test_clear_rows_non_consecutive_rows():
    """Test clearing non-consecutive rows."""
    playfield = Playfield()
    
    # Fill rows 15 and 19
    for x in range(10):
        playfield.set_cell(x, 15, (255, 0, 0))
        playfield.set_cell(x, 19, (0, 0, 255))
    
    # Place blocks between them
    playfield.set_cell(5, 17, (0, 255, 0))
    
    # Clear rows 15 and 19
    playfield.clear_rows([15, 19])
    
    # Row 19 should be empty
    for x in range(10):
        assert playfield.get_cell(x, 19) is None
    
    # Block at 17 should move down to 18 (one cleared row below it)
    assert playfield.get_cell(5, 18) == (0, 255, 0)
    assert playfield.get_cell(5, 17) is None


def test_clear_rows_preserves_colors():
    """Test that clear_rows preserves block colors when shifting down."""
    playfield = Playfield()
    
    # Create a pattern with different colors
    playfield.set_cell(0, 10, (255, 0, 0))    # Red
    playfield.set_cell(1, 10, (0, 255, 0))    # Green
    playfield.set_cell(2, 10, (0, 0, 255))    # Blue
    
    # Fill row 19 to clear it
    for x in range(10):
        playfield.set_cell(x, 19, (128, 128, 128))
    
    # Clear row 19
    playfield.clear_rows([19])
    
    # Colors should be preserved after shifting down by 1
    # Row 10 becomes row 11
    assert playfield.get_cell(0, 11) == (255, 0, 0)
    assert playfield.get_cell(1, 11) == (0, 255, 0)
    assert playfield.get_cell(2, 11) == (0, 0, 255)
    
    # Original row 10 should now be empty (new row added at top)
    assert playfield.get_cell(0, 10) is None
    assert playfield.get_cell(1, 10) is None
    assert playfield.get_cell(2, 10) is None


def test_clear_rows_adds_empty_rows_at_top():
    """Test that clear_rows adds empty rows at the top."""
    playfield = Playfield()
    
    # Fill bottom 3 rows
    for y in [17, 18, 19]:
        for x in range(10):
            playfield.set_cell(x, y, (255, 0, 0))
    
    # Place a block at top
    playfield.set_cell(5, 0, (0, 255, 0))
    
    # Clear all 3 bottom rows
    playfield.clear_rows([17, 18, 19])
    
    # Top 3 rows should be empty (new rows added)
    for y in [0, 1, 2]:
        for x in range(10):
            if not (x == 5 and y == 3):  # Except the shifted block
                assert playfield.get_cell(x, y) is None
    
    # Block that was at row 0 should now be at row 3
    assert playfield.get_cell(5, 3) == (0, 255, 0)
    assert playfield.get_cell(5, 0) is None


def test_clear_rows_complex_scenario():
    """Test clear_rows with a complex playfield configuration."""
    playfield = Playfield()
    
    # Create a complex pattern
    # Row 19: complete
    for x in range(10):
        playfield.set_cell(x, 19, (255, 0, 0))
    
    # Row 18: partial
    for x in range(5):
        playfield.set_cell(x, 18, (0, 255, 0))
    
    # Row 17: complete
    for x in range(10):
        playfield.set_cell(x, 17, (0, 0, 255))
    
    # Row 16: partial
    playfield.set_cell(3, 16, (255, 255, 0))
    playfield.set_cell(7, 16, (255, 0, 255))
    
    # Clear rows 17 and 19
    playfield.clear_rows([17, 19])
    
    # After clearing 2 rows, everything shifts down by 2
    # Row 18 (partial green) becomes row 19
    for x in range(5):
        assert playfield.get_cell(x, 19) == (0, 255, 0)
    for x in range(5, 10):
        assert playfield.get_cell(x, 19) is None
    
    # Row 16 (partial yellow/magenta) becomes row 18
    assert playfield.get_cell(3, 18) == (255, 255, 0)
    assert playfield.get_cell(7, 18) == (255, 0, 255)
    
    # Other cells in row 18 should be empty
    for x in range(10):
        if x not in [3, 7]:
            assert playfield.get_cell(x, 18) is None


# ============================================================================
# Property-Based Tests
# ============================================================================

# Custom strategies for property-based testing
def valid_position():
    """Strategy for generating valid playfield positions."""
    return st.tuples(
        st.integers(min_value=0, max_value=PLAYFIELD_WIDTH - 1),   # x
        st.integers(min_value=0, max_value=PLAYFIELD_HEIGHT - 1)   # y
    )


def rgb_color():
    """Strategy for generating valid RGB color tuples."""
    return st.tuples(
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255)
    )


@settings(max_examples=100)
@given(position=valid_position())
def test_property_1_playfield_dimensions_invariant(position):
    """Property 1: Playfield Dimensions Invariant.
    
    For any Playfield instance, the grid dimensions shall always be
    exactly 10 columns and 20 rows.
    
    Feature: tetris-clone, Property 1: Playfield Dimensions Invariant
    Validates: Requirements 1.1
    """
    playfield = Playfield()
    
    # Dimensions are always 10×20
    assert playfield.width == 10, f"Width is {playfield.width}, expected 10"
    assert playfield.height == 20, f"Height is {playfield.height}, expected 20"
    
    # Grid structure matches dimensions
    assert len(playfield.grid) == 20, f"Grid has {len(playfield.grid)} rows, expected 20"
    for row in playfield.grid:
        assert len(row) == 10, f"Row has {len(row)} columns, expected 10"


@settings(max_examples=100)
@given(position=valid_position(), color=st.one_of(st.none(), rgb_color()))
def test_property_2_playfield_state_accessibility(position, color):
    """Property 2: Playfield State Accessibility.
    
    For any Playfield instance and any valid coordinates (x, y) where
    0 ≤ x < 10 and 0 ≤ y < 20, querying the cell state shall return
    either None (empty) or a valid RGB color tuple.
    
    Feature: tetris-clone, Property 2: Playfield State Accessibility
    Validates: Requirements 1.4
    """
    playfield = Playfield()
    x, y = position
    
    # Set the cell to the generated color (or None)
    playfield.set_cell(x, y, color)
    
    # Get the cell value
    result = playfield.get_cell(x, y)
    
    # Result should match what we set
    assert result == color, f"Expected {color}, got {result}"
    
    # Result should be either None or a 3-tuple of integers
    if result is not None:
        assert isinstance(result, tuple), f"Result is {type(result)}, expected tuple"
        assert len(result) == 3, f"Result has {len(result)} elements, expected 3"
        for component in result:
            assert isinstance(component, int), f"Color component is {type(component)}, expected int"
            assert 0 <= component <= 255, f"Color component {component} out of range [0, 255]"


@settings(max_examples=100)
@given(
    shape_type=st.sampled_from(['I', 'O', 'T', 'L', 'J', 'S', 'Z']),
    rotation=st.integers(min_value=0, max_value=3)
)
def test_property_3_boundary_collision_prevention(shape_type, rotation):
    """Property 3: Boundary Collision Prevention.
    
    For any tetromino and any playfield state, attempting to move the
    tetromino beyond the left boundary (x < 0) or right boundary
    (x + width > 10) shall be prevented.
    
    Feature: tetris-clone, Property 3: Boundary Collision Prevention
    Validates: Requirements 1.5, 1.6, 3.5, 3.6
    """
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Test left boundary - tetromino far to the left should be invalid
    tetromino = Tetromino(shape_type=shape_type, x=-5, y=10, rotation=rotation)
    assert playfield.is_valid_position(tetromino) is False, \
        f"Tetromino {shape_type} at x=-5 should be invalid (left boundary)"
    
    # Test right boundary - tetromino far to the right should be invalid
    tetromino = Tetromino(shape_type=shape_type, x=15, y=10, rotation=rotation)
    assert playfield.is_valid_position(tetromino) is False, \
        f"Tetromino {shape_type} at x=15 should be invalid (right boundary)"
    
    # Test bottom boundary - tetromino far below should be invalid
    tetromino = Tetromino(shape_type=shape_type, x=5, y=25, rotation=rotation)
    assert playfield.is_valid_position(tetromino) is False, \
        f"Tetromino {shape_type} at y=25 should be invalid (bottom boundary)"


@settings(max_examples=100)
@given(
    shape_type=st.sampled_from(['I', 'O', 'T', 'L', 'J', 'S', 'Z']),
    x=st.integers(min_value=1, max_value=8),
    y=st.integers(min_value=5, max_value=15),
    rotation=st.integers(min_value=0, max_value=3)
)
def test_property_8_collision_detection_correctness(shape_type, x, y, rotation):
    """Property 8: Collision Detection Correctness.
    
    For any tetromino position and any playfield state with stopped blocks,
    attempting to move the tetromino into a position where any of its blocks
    would overlap with stopped blocks shall be prevented.
    
    Feature: tetris-clone, Property 8: Collision Detection Correctness
    Validates: Requirements 3.7
    """
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Create a tetromino at the given position
    tetromino = Tetromino(shape_type=shape_type, x=x, y=y, rotation=rotation)
    
    # If the position is valid on empty playfield, test collision detection
    if playfield.is_valid_position(tetromino):
        # Get the blocks of this tetromino
        blocks = tetromino.get_absolute_blocks()
        
        # Place a stopped block at one of the tetromino's positions
        if blocks:
            block_x, block_y = blocks[0]
            if 0 <= block_x < 10 and 0 <= block_y < 20:
                playfield.set_cell(block_x, block_y, (255, 0, 0))
                
                # Now the same position should be invalid
                assert playfield.is_valid_position(tetromino) is False, \
                    f"Tetromino {shape_type} at ({x}, {y}) should be invalid after placing block at ({block_x}, {block_y})"
    
    # Test that empty playfield allows valid positions
    empty_playfield = Playfield()
    tetromino_center = Tetromino(shape_type=shape_type, x=5, y=10, rotation=rotation)
    # This might be valid or invalid depending on the shape, but should be consistent
    result1 = empty_playfield.is_valid_position(tetromino_center)
    result2 = empty_playfield.is_valid_position(tetromino_center)
    assert result1 == result2, "is_valid_position should be deterministic"


@settings(max_examples=100)
@given(
    row_index=st.integers(min_value=0, max_value=PLAYFIELD_HEIGHT - 1),
    num_filled=st.integers(min_value=0, max_value=PLAYFIELD_WIDTH)
)
def test_property_13_complete_row_detection(row_index, num_filled):
    """Property 13: Complete Row Detection.
    
    For any playfield state, a row at index y is complete if and only if
    all 10 positions in that row contain non-None color values.
    
    Feature: tetris-clone, Property 13: Complete Row Detection
    Validates: Requirements 5.1
    """
    playfield = Playfield()
    
    # Fill num_filled cells in the row
    for x in range(num_filled):
        playfield.set_cell(x, row_index, (255, 0, 0))
    
    # Get complete rows
    complete_rows = playfield.get_complete_rows()
    
    # Row should be complete if and only if all 10 cells are filled
    if num_filled == PLAYFIELD_WIDTH:
        assert row_index in complete_rows, \
            f"Row {row_index} with all {PLAYFIELD_WIDTH} cells filled should be complete"
    else:
        assert row_index not in complete_rows, \
            f"Row {row_index} with only {num_filled}/{PLAYFIELD_WIDTH} cells filled should not be complete"


@settings(max_examples=100)
@given(
    rows_to_fill=st.lists(
        st.integers(min_value=0, max_value=PLAYFIELD_HEIGHT - 1),
        min_size=1,
        max_size=4,
        unique=True
    )
)
def test_property_14_row_clearing_empties_rows(rows_to_fill):
    """Property 14: Row Clearing Empties Rows.
    
    For any playfield state with complete rows, clearing those rows shall
    result in those row indices containing only None values (empty cells).
    
    Feature: tetris-clone, Property 14: Row Clearing Empties Rows
    Validates: Requirements 5.2
    """
    playfield = Playfield()
    
    # Fill the specified rows completely
    for row in rows_to_fill:
        for x in range(PLAYFIELD_WIDTH):
            playfield.set_cell(x, row, (255, 0, 0))
    
    # Verify rows are complete
    complete_rows = playfield.get_complete_rows()
    for row in rows_to_fill:
        assert row in complete_rows, f"Row {row} should be complete after filling"
    
    # Clear the rows
    playfield.clear_rows(rows_to_fill)
    
    # After clearing, the playfield should have no complete rows
    # (the cleared rows are now at the top and empty)
    complete_rows_after = playfield.get_complete_rows()
    assert len(complete_rows_after) == 0, \
        f"After clearing rows, no complete rows should exist, but found {complete_rows_after}"
    
    # The top N rows (where N = number of cleared rows) should be empty
    num_cleared = len(rows_to_fill)
    for y in range(num_cleared):
        for x in range(PLAYFIELD_WIDTH):
            assert playfield.get_cell(x, y) is None, \
                f"Cell ({x}, {y}) should be empty after clearing {num_cleared} rows"


@settings(max_examples=100)
@given(
    clear_row=st.integers(min_value=1, max_value=PLAYFIELD_HEIGHT - 1),
    blocks_above=st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=PLAYFIELD_WIDTH - 1),
            st.integers(min_value=0, max_value=PLAYFIELD_HEIGHT - 2)
        ),
        min_size=0,
        max_size=10,
        unique=True
    ),
    color=rgb_color()
)
def test_property_15_row_clearing_gravity(clear_row, blocks_above, color):
    """Property 15: Row Clearing Gravity.
    
    For any playfield state where row y is cleared, all blocks in rows
    above y (rows 0 to y-1) shall move down by one row, preserving their
    colors and relative positions.
    
    Feature: tetris-clone, Property 15: Row Clearing Gravity
    Validates: Requirements 5.3, 5.5
    """
    from hypothesis import assume
    
    playfield = Playfield()
    
    # Filter blocks to only those above the clear_row
    blocks_above_clear = [(x, y) for x, y in blocks_above if y < clear_row]
    
    # Place blocks above the row to be cleared
    for x, y in blocks_above_clear:
        playfield.set_cell(x, y, color)
    
    # Fill the row to be cleared completely
    for x in range(PLAYFIELD_WIDTH):
        playfield.set_cell(x, clear_row, (128, 128, 128))
    
    # Record the positions and colors of blocks above the cleared row
    blocks_before = {}
    for x, y in blocks_above_clear:
        blocks_before[(x, y)] = playfield.get_cell(x, y)
    
    # Clear the row
    playfield.clear_rows([clear_row])
    
    # Verify that blocks moved down by 1 and preserved their colors
    for (x, y), original_color in blocks_before.items():
        new_y = y + 1
        assert playfield.get_cell(x, new_y) == original_color, \
            f"Block at ({x}, {y}) should move to ({x}, {new_y}) with color {original_color}"
    
    # Verify that the top row is now empty (new row added at top)
    for x in range(PLAYFIELD_WIDTH):
        assert playfield.get_cell(x, 0) is None, \
            f"Top row cell ({x}, 0) should be empty after clearing a row"


@settings(max_examples=100)
@given(
    num_rows_to_clear=st.integers(min_value=1, max_value=4),
    start_row=st.integers(min_value=0, max_value=PLAYFIELD_HEIGHT - 4)
)
def test_property_16_multiple_row_clearing(num_rows_to_clear, start_row):
    """Property 16: Multiple Row Clearing.
    
    For any playfield state with N complete rows, clearing all complete
    rows shall remove exactly N rows and shift all rows above the highest
    cleared row down by N positions.
    
    Feature: tetris-clone, Property 16: Multiple Row Clearing
    Validates: Requirements 5.4
    """
    from hypothesis import assume
    
    # Ensure we don't go out of bounds
    assume(start_row + num_rows_to_clear <= PLAYFIELD_HEIGHT)
    
    playfield = Playfield()
    
    # Create rows to clear (consecutive for simplicity)
    rows_to_clear = list(range(start_row, start_row + num_rows_to_clear))
    
    # Fill these rows completely
    for row in rows_to_clear:
        for x in range(PLAYFIELD_WIDTH):
            playfield.set_cell(x, row, (255, 0, 0))
    
    # Place some blocks above the cleared rows
    test_color = (0, 255, 0)
    blocks_above = []
    if start_row > 0:
        # Place a block in the row above the cleared section
        test_row = start_row - 1
        test_x = 5
        playfield.set_cell(test_x, test_row, test_color)
        blocks_above.append((test_x, test_row))
    
    # Clear the rows
    playfield.clear_rows(rows_to_clear)
    
    # Verify that exactly N rows were cleared
    # The top N rows should now be empty
    for y in range(num_rows_to_clear):
        for x in range(PLAYFIELD_WIDTH):
            assert playfield.get_cell(x, y) is None, \
                f"Top row {y} should be empty after clearing {num_rows_to_clear} rows"
    
    # Verify that blocks above moved down by N positions
    for original_x, original_y in blocks_above:
        new_y = original_y + num_rows_to_clear
        assert playfield.get_cell(original_x, new_y) == test_color, \
            f"Block at ({original_x}, {original_y}) should move to ({original_x}, {new_y})"
    
    # Verify no complete rows remain
    complete_rows = playfield.get_complete_rows()
    assert len(complete_rows) == 0, \
        f"After clearing, no complete rows should remain, but found {complete_rows}"


def test_is_game_over_empty_playfield():
    """Test that is_game_over returns False for an empty playfield."""
    playfield = Playfield()
    
    assert playfield.is_game_over() is False


def test_is_game_over_blocks_not_in_top_row():
    """Test that is_game_over returns False when blocks exist but not in top row."""
    playfield = Playfield()
    
    # Place blocks in various rows except the top row
    playfield.set_cell(5, 1, (255, 0, 0))
    playfield.set_cell(3, 5, (0, 255, 0))
    playfield.set_cell(7, 10, (0, 0, 255))
    playfield.set_cell(2, 19, (255, 255, 0))
    
    assert playfield.is_game_over() is False


def test_is_game_over_single_block_in_top_row():
    """Test that is_game_over returns True when a single block exists in top row."""
    playfield = Playfield()
    
    # Place a single block in the top row
    playfield.set_cell(5, 0, (255, 0, 0))
    
    assert playfield.is_game_over() is True


def test_is_game_over_multiple_blocks_in_top_row():
    """Test that is_game_over returns True when multiple blocks exist in top row."""
    playfield = Playfield()
    
    # Place multiple blocks in the top row
    playfield.set_cell(0, 0, (255, 0, 0))
    playfield.set_cell(5, 0, (0, 255, 0))
    playfield.set_cell(9, 0, (0, 0, 255))
    
    assert playfield.is_game_over() is True


def test_is_game_over_full_top_row():
    """Test that is_game_over returns True when entire top row is filled."""
    playfield = Playfield()
    
    # Fill the entire top row
    for x in range(10):
        playfield.set_cell(x, 0, (128, 128, 128))
    
    assert playfield.is_game_over() is True


def test_is_game_over_after_adding_tetromino_to_top():
    """Test that is_game_over returns True after adding a tetromino to top row."""
    from tetris.models.tetromino import Tetromino
    
    playfield = Playfield()
    
    # Initially not game over
    assert playfield.is_game_over() is False
    
    # Add a tetromino that has blocks in the top row
    # I-piece horizontal at y=0: blocks at (0,0), (1,0), (2,0), (3,0)
    tetromino = Tetromino(shape_type='I', x=0, y=0, rotation=0)
    playfield.add_tetromino(tetromino)
    
    # Now should be game over
    assert playfield.is_game_over() is True


def test_is_game_over_playfield_almost_full():
    """Test that is_game_over only triggers when top row has blocks."""
    playfield = Playfield()
    
    # Fill all rows except the top row
    for y in range(1, 20):
        for x in range(10):
            playfield.set_cell(x, y, (255, 0, 0))
    
    # Should not be game over yet (top row is empty)
    assert playfield.is_game_over() is False
    
    # Add a single block to top row
    playfield.set_cell(0, 0, (255, 0, 0))
    
    # Now should be game over
    assert playfield.is_game_over() is True
