"""Unit tests for the Tetromino class.

This module tests tetromino shape definitions, colors, movement, and rotation.
It includes both specific example-based tests and property-based tests using Hypothesis.
"""

import pytest
from hypothesis import given, settings, strategies as st

from tetris.models.tetromino import Tetromino, TETROMINO_COLORS, TETROMINO_SHAPES


# ============================================================================
# Unit Tests - Specific Examples
# ============================================================================

class TestTetrominoCreation:
    """Test tetromino creation and initialization."""
    
    def test_create_i_tetromino(self):
        """Test creating an I-piece with correct color and attributes."""
        tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        assert tetromino.shape_type == 'I'
        assert tetromino.x == 5
        assert tetromino.y == 10
        assert tetromino.rotation == 0
        assert tetromino.color == (0, 255, 255)  # Cyan
    
    def test_create_o_tetromino(self):
        """Test creating an O-piece with correct color."""
        tetromino = Tetromino(shape_type='O', x=3, y=7, rotation=0)
        assert tetromino.shape_type == 'O'
        assert tetromino.color == (255, 255, 0)  # Yellow
    
    def test_create_t_tetromino(self):
        """Test creating a T-piece with correct color."""
        tetromino = Tetromino(shape_type='T', x=4, y=2, rotation=0)
        assert tetromino.shape_type == 'T'
        assert tetromino.color == (128, 0, 128)  # Purple
    
    def test_create_l_tetromino(self):
        """Test creating an L-piece with correct color."""
        tetromino = Tetromino(shape_type='L', x=6, y=8, rotation=0)
        assert tetromino.shape_type == 'L'
        assert tetromino.color == (255, 165, 0)  # Orange
    
    def test_create_j_tetromino(self):
        """Test creating a J-piece with correct color."""
        tetromino = Tetromino(shape_type='J', x=2, y=5, rotation=0)
        assert tetromino.shape_type == 'J'
        assert tetromino.color == (0, 0, 255)  # Dark Blue
    
    def test_create_s_tetromino(self):
        """Test creating an S-piece with correct color."""
        tetromino = Tetromino(shape_type='S', x=7, y=3, rotation=0)
        assert tetromino.shape_type == 'S'
        assert tetromino.color == (0, 255, 0)  # Green
    
    def test_create_z_tetromino(self):
        """Test creating a Z-piece with correct color."""
        tetromino = Tetromino(shape_type='Z', x=1, y=9, rotation=0)
        assert tetromino.shape_type == 'Z'
        assert tetromino.color == (255, 0, 0)  # Red
    
    def test_invalid_shape_type_raises_error(self):
        """Test that invalid shape type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid shape_type"):
            Tetromino(shape_type='X', x=0, y=0, rotation=0)
    
    def test_invalid_rotation_raises_error(self):
        """Test that invalid rotation value raises ValueError."""
        with pytest.raises(ValueError, match="Invalid rotation"):
            Tetromino(shape_type='I', x=0, y=0, rotation=4)
        
        with pytest.raises(ValueError, match="Invalid rotation"):
            Tetromino(shape_type='I', x=0, y=0, rotation=-1)


class TestTetrominoShapes:
    """Test that tetromino shapes have correct configurations."""
    
    def test_i_piece_has_four_blocks(self):
        """Test I-piece has exactly 4 blocks in horizontal configuration."""
        tetromino = Tetromino(shape_type='I', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # Horizontal: [(0,0), (1,0), (2,0), (3,0)]
        assert blocks == [(0, 0), (1, 0), (2, 0), (3, 0)]
    
    def test_i_piece_vertical_rotation(self):
        """Test I-piece vertical configuration after rotation."""
        tetromino = Tetromino(shape_type='I', x=0, y=0, rotation=1)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # Vertical: [(1,0), (1,1), (1,2), (1,3)]
        assert blocks == [(1, 0), (1, 1), (1, 2), (1, 3)]
    
    def test_o_piece_is_square(self):
        """Test O-piece is a 2x2 square."""
        tetromino = Tetromino(shape_type='O', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # Square: [(0,0), (1,0), (0,1), (1,1)]
        assert blocks == [(0, 0), (1, 0), (0, 1), (1, 1)]
    
    def test_o_piece_same_in_all_rotations(self):
        """Test O-piece looks the same in all rotation states."""
        expected = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for rotation in range(4):
            tetromino = Tetromino(shape_type='O', x=0, y=0, rotation=rotation)
            assert tetromino.get_blocks() == expected
    
    def test_t_piece_shape(self):
        """Test T-piece has correct T-shape configuration."""
        tetromino = Tetromino(shape_type='T', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # T pointing up: [(1,0), (0,1), (1,1), (2,1)]
        assert blocks == [(1, 0), (0, 1), (1, 1), (2, 1)]
    
    def test_l_piece_shape(self):
        """Test L-piece has correct L-shape configuration."""
        tetromino = Tetromino(shape_type='L', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # L with base at bottom, extending right: [(2,0), (0,1), (1,1), (2,1)]
        assert blocks == [(2, 0), (0, 1), (1, 1), (2, 1)]
    
    def test_j_piece_shape(self):
        """Test J-piece has correct J-shape configuration."""
        tetromino = Tetromino(shape_type='J', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # J with base at bottom, extending left: [(0,0), (0,1), (1,1), (2,1)]
        assert blocks == [(0, 0), (0, 1), (1, 1), (2, 1)]
    
    def test_s_piece_shape(self):
        """Test S-piece has correct zigzag configuration."""
        tetromino = Tetromino(shape_type='S', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # S horizontal: [(1,0), (2,0), (0,1), (1,1)]
        assert blocks == [(1, 0), (2, 0), (0, 1), (1, 1)]
    
    def test_z_piece_shape(self):
        """Test Z-piece has correct zigzag configuration."""
        tetromino = Tetromino(shape_type='Z', x=0, y=0, rotation=0)
        blocks = tetromino.get_blocks()
        assert len(blocks) == 4
        # Z horizontal: [(0,0), (1,0), (1,1), (2,1)]
        assert blocks == [(0, 0), (1, 0), (1, 1), (2, 1)]


class TestTetrominoMovement:
    """Test tetromino movement operations."""
    
    def test_move_left(self):
        """Test moving tetromino left decreases x coordinate."""
        tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        moved = tetromino.move(-1, 0)
        
        assert moved.x == 4
        assert moved.y == 10
        assert moved.shape_type == 'I'
        assert moved.rotation == 0
        # Original unchanged (immutable)
        assert tetromino.x == 5
    
    def test_move_right(self):
        """Test moving tetromino right increases x coordinate."""
        tetromino = Tetromino(shape_type='T', x=3, y=7, rotation=0)
        moved = tetromino.move(1, 0)
        
        assert moved.x == 4
        assert moved.y == 7
    
    def test_move_down(self):
        """Test moving tetromino down increases y coordinate."""
        tetromino = Tetromino(shape_type='O', x=5, y=5, rotation=0)
        moved = tetromino.move(0, 1)
        
        assert moved.x == 5
        assert moved.y == 6
    
    def test_move_diagonal(self):
        """Test moving tetromino diagonally."""
        tetromino = Tetromino(shape_type='L', x=4, y=8, rotation=0)
        moved = tetromino.move(2, 3)
        
        assert moved.x == 6
        assert moved.y == 11
    
    def test_move_returns_new_instance(self):
        """Test that move returns a new instance, not modifying original."""
        original = Tetromino(shape_type='J', x=5, y=10, rotation=0)
        moved = original.move(1, 1)
        
        assert original is not moved
        assert original.x == 5
        assert original.y == 10
        assert moved.x == 6
        assert moved.y == 11


class TestTetrominoRotation:
    """Test tetromino rotation operations."""
    
    def test_rotate_clockwise_increments_rotation(self):
        """Test rotating clockwise increments rotation state."""
        tetromino = Tetromino(shape_type='T', x=5, y=10, rotation=0)
        rotated = tetromino.rotate_clockwise()
        
        assert rotated.rotation == 1
        assert rotated.x == 5  # Position unchanged
        assert rotated.y == 10
        assert rotated.shape_type == 'T'
    
    def test_rotate_wraps_around(self):
        """Test rotation wraps from 3 back to 0."""
        tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=3)
        rotated = tetromino.rotate_clockwise()
        
        assert rotated.rotation == 0
    
    def test_rotate_preserves_position(self):
        """Test rotation preserves center position."""
        tetromino = Tetromino(shape_type='L', x=7, y=12, rotation=0)
        rotated = tetromino.rotate_clockwise()
        
        assert rotated.x == 7
        assert rotated.y == 12
    
    def test_rotate_returns_new_instance(self):
        """Test that rotate returns a new instance."""
        original = Tetromino(shape_type='S', x=5, y=10, rotation=0)
        rotated = original.rotate_clockwise()
        
        assert original is not rotated
        assert original.rotation == 0
        assert rotated.rotation == 1
    
    def test_rotate_four_times_returns_to_original(self):
        """Test rotating 4 times returns to original configuration."""
        tetromino = Tetromino(shape_type='T', x=5, y=10, rotation=0)
        original_blocks = tetromino.get_blocks()
        
        rotated = tetromino
        for _ in range(4):
            rotated = rotated.rotate_clockwise()
        
        assert rotated.rotation == 0
        assert rotated.get_blocks() == original_blocks


class TestAbsoluteBlocks:
    """Test calculation of absolute block positions."""
    
    def test_absolute_blocks_at_origin(self):
        """Test absolute blocks when tetromino is at origin."""
        tetromino = Tetromino(shape_type='O', x=0, y=0, rotation=0)
        absolute = tetromino.get_absolute_blocks()
        relative = tetromino.get_blocks()
        
        # At origin, absolute should equal relative
        assert absolute == relative
    
    def test_absolute_blocks_with_offset(self):
        """Test absolute blocks with position offset."""
        tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        absolute = tetromino.get_absolute_blocks()
        
        # I-piece at rotation 0: [(0,0), (1,0), (2,0), (3,0)]
        # With offset (5, 10): [(5,10), (6,10), (7,10), (8,10)]
        expected = [(5, 10), (6, 10), (7, 10), (8, 10)]
        assert absolute == expected
    
    def test_absolute_blocks_count(self):
        """Test that absolute blocks always has 4 elements."""
        tetromino = Tetromino(shape_type='T', x=3, y=7, rotation=2)
        absolute = tetromino.get_absolute_blocks()
        
        assert len(absolute) == 4


class TestTetrominoEquality:
    """Test tetromino equality comparison."""
    
    def test_equal_tetrominoes(self):
        """Test that tetrominoes with same attributes are equal."""
        t1 = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        t2 = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        
        assert t1 == t2
    
    def test_different_position_not_equal(self):
        """Test that tetrominoes with different positions are not equal."""
        t1 = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        t2 = Tetromino(shape_type='I', x=6, y=10, rotation=0)
        
        assert t1 != t2
    
    def test_different_rotation_not_equal(self):
        """Test that tetrominoes with different rotations are not equal."""
        t1 = Tetromino(shape_type='T', x=5, y=10, rotation=0)
        t2 = Tetromino(shape_type='T', x=5, y=10, rotation=1)
        
        assert t1 != t2
    
    def test_different_shape_not_equal(self):
        """Test that tetrominoes with different shapes are not equal."""
        t1 = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        t2 = Tetromino(shape_type='O', x=5, y=10, rotation=0)
        
        assert t1 != t2


# ============================================================================
# Property-Based Tests
# ============================================================================

# Custom strategies for generating test data
def tetromino_type():
    """Strategy for generating valid tetromino types."""
    return st.sampled_from(['I', 'O', 'T', 'L', 'J', 'S', 'Z'])


def valid_rotation():
    """Strategy for generating valid rotation values."""
    return st.integers(min_value=0, max_value=3)


def tetromino():
    """Strategy for generating random tetrominoes."""
    return st.builds(
        Tetromino,
        shape_type=tetromino_type(),
        x=st.integers(min_value=-5, max_value=15),
        y=st.integers(min_value=-5, max_value=25),
        rotation=valid_rotation()
    )


class TestTetrominoProperties:
    """Property-based tests for tetromino invariants."""
    
    @settings(max_examples=100)
    @given(
        shape_type=tetromino_type(),
        rotation=valid_rotation()
    )
    def test_property_4_tetromino_block_count_invariant(self, shape_type, rotation):
        """Property 4: Any tetromino always has exactly 4 blocks.
        
        Feature: tetris-clone, Property 4: Tetromino Block Count Invariant
        Validates: Requirements 2.1-2.8
        """
        tetromino = Tetromino(shape_type=shape_type, x=0, y=0, rotation=rotation)
        blocks = tetromino.get_absolute_blocks()
        
        assert len(blocks) == 4, (
            f"Tetromino {shape_type} at rotation {rotation} has {len(blocks)} blocks, "
            f"expected 4"
        )
    
    @settings(max_examples=100)
    @given(tetromino=tetromino())
    def test_property_6_rotation_preserves_block_count(self, tetromino):
        """Property 6: Rotating clockwise preserves block count and color.
        
        Feature: tetris-clone, Property 6: Rotation Preserves Block Count
        Validates: Requirements 3.3
        """
        rotated = tetromino.rotate_clockwise()
        
        # Check block count preserved
        assert len(rotated.get_absolute_blocks()) == 4, (
            f"Rotated tetromino has {len(rotated.get_absolute_blocks())} blocks, "
            f"expected 4"
        )
        
        # Check color preserved
        assert rotated.color == tetromino.color, (
            f"Rotation changed color from {tetromino.color} to {rotated.color}"
        )
        
        # Check shape type preserved
        assert rotated.shape_type == tetromino.shape_type
    
    @settings(max_examples=100)
    @given(tetromino=tetromino())
    def test_property_10_rotation_center_preservation(self, tetromino):
        """Property 10: Rotation preserves center position.
        
        Feature: tetris-clone, Property 10: Rotation Center Preservation
        Validates: Requirements 3.9
        """
        rotated = tetromino.rotate_clockwise()
        
        assert rotated.x == tetromino.x, (
            f"Rotation changed x from {tetromino.x} to {rotated.x}"
        )
        assert rotated.y == tetromino.y, (
            f"Rotation changed y from {tetromino.y} to {rotated.y}"
        )
    
    @settings(max_examples=100)
    @given(
        tetromino=tetromino(),
        dx=st.integers(min_value=-10, max_value=10),
        dy=st.integers(min_value=-10, max_value=10)
    )
    def test_property_5_movement_delta_correctness(self, tetromino, dx, dy):
        """Property 5: Movement delta is applied correctly.
        
        Feature: tetris-clone, Property 5: Movement Delta Correctness
        Validates: Requirements 3.1, 3.2
        """
        moved = tetromino.move(dx, dy)
        
        assert moved.x == tetromino.x + dx, (
            f"Expected x={tetromino.x + dx}, got x={moved.x}"
        )
        assert moved.y == tetromino.y + dy, (
            f"Expected y={tetromino.y + dy}, got y={moved.y}"
        )
        
        # Verify other attributes unchanged
        assert moved.shape_type == tetromino.shape_type
        assert moved.rotation == tetromino.rotation
        assert moved.color == tetromino.color
    
    @settings(max_examples=100)
    @given(tetromino=tetromino())
    def test_immutability_move(self, tetromino):
        """Test that move operation doesn't modify original tetromino."""
        original_x = tetromino.x
        original_y = tetromino.y
        
        moved = tetromino.move(5, 3)
        
        # Original unchanged
        assert tetromino.x == original_x
        assert tetromino.y == original_y
        
        # New instance created
        assert moved is not tetromino
    
    @settings(max_examples=100)
    @given(tetromino=tetromino())
    def test_immutability_rotate(self, tetromino):
        """Test that rotate operation doesn't modify original tetromino."""
        original_rotation = tetromino.rotation
        
        rotated = tetromino.rotate_clockwise()
        
        # Original unchanged
        assert tetromino.rotation == original_rotation
        
        # New instance created
        assert rotated is not tetromino
    
    @settings(max_examples=100)
    @given(tetromino=tetromino())
    def test_four_rotations_return_to_start(self, tetromino):
        """Test that four clockwise rotations return to original state."""
        result = tetromino
        for _ in range(4):
            result = result.rotate_clockwise()
        
        assert result.rotation == tetromino.rotation
        assert result.get_blocks() == tetromino.get_blocks()
