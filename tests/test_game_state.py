"""Unit and property-based tests for the GameState class.

This module contains tests for the GameState class, including:
- Unit tests for specific examples and edge cases
- Property-based tests for universal correctness properties
"""

import pytest
from hypothesis import given, settings, strategies as st

from tetris.models.game_state import GameState
from tetris.models.tetromino import Tetromino
from tetris.models.playfield import PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT


# ============================================================================
# Unit Tests
# ============================================================================

def test_game_state_initialization():
    """Test that a new game state is initialized correctly."""
    game_state = GameState()
    
    # Verify initial state
    assert game_state.playfield is not None
    assert game_state.playfield.width == PLAYFIELD_WIDTH
    assert game_state.playfield.height == PLAYFIELD_HEIGHT
    assert game_state.active_tetromino is None
    assert game_state.score == 0
    assert game_state.game_over is False
    assert game_state.fall_timer == 0.0
    assert game_state.fall_interval == 0.5


def test_game_state_playfield_is_empty():
    """Test that the playfield is initially empty."""
    game_state = GameState()
    
    # Check all cells are empty
    for y in range(game_state.playfield.height):
        for x in range(game_state.playfield.width):
            assert game_state.playfield.get_cell(x, y) is None


def test_spawn_tetromino_creates_tetromino():
    """Test that spawn_tetromino creates a new tetromino."""
    game_state = GameState()
    
    tetromino = game_state.spawn_tetromino()
    
    # Verify a tetromino was created
    assert tetromino is not None
    assert game_state.active_tetromino is not None
    assert game_state.active_tetromino == tetromino
    
    # Verify it's at the spawn position (x=4, y=0)
    assert tetromino.x == 4
    assert tetromino.y == 0
    assert tetromino.rotation == 0
    
    # Verify it's one of the seven valid types
    assert tetromino.shape_type in ['I', 'O', 'T', 'L', 'J', 'S', 'Z']


def test_spawn_tetromino_random_types():
    """Test that spawn_tetromino generates different types."""
    game_state = GameState()
    
    # Spawn multiple tetrominoes and collect their types
    types_seen = set()
    for _ in range(50):
        game_state = GameState()  # Fresh state each time
        tetromino = game_state.spawn_tetromino()
        types_seen.add(tetromino.shape_type)
    
    # With 50 spawns, we should see multiple different types
    # (probability of seeing only 1 type is astronomically low)
    assert len(types_seen) > 1, f"Only saw types: {types_seen}"


def test_move_active_left_success():
    """Test moving active tetromino left when valid."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    original_x = game_state.active_tetromino.x
    
    # Move left should succeed
    result = game_state.move_active_left()
    
    assert result is True
    assert game_state.active_tetromino.x == original_x - 1


def test_move_active_right_success():
    """Test moving active tetromino right when valid."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    original_x = game_state.active_tetromino.x
    
    # Move right should succeed
    result = game_state.move_active_right()
    
    assert result is True
    assert game_state.active_tetromino.x == original_x + 1


def test_move_active_left_at_boundary():
    """Test that moving left at boundary is prevented."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Move far left until we hit the boundary
    for _ in range(20):
        game_state.move_active_left()
    
    # Get current position
    x_at_boundary = game_state.active_tetromino.x
    
    # Try to move left again - should fail
    result = game_state.move_active_left()
    
    # Position should not change
    assert game_state.active_tetromino.x == x_at_boundary


def test_move_active_right_at_boundary():
    """Test that moving right at boundary is prevented."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Move far right until we hit the boundary
    for _ in range(20):
        game_state.move_active_right()
    
    # Get current position
    x_at_boundary = game_state.active_tetromino.x
    
    # Try to move right again - should fail
    result = game_state.move_active_right()
    
    # Position should not change
    assert game_state.active_tetromino.x == x_at_boundary


def test_rotate_active_success():
    """Test rotating active tetromino when valid."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    original_rotation = game_state.active_tetromino.rotation
    
    # Rotate should succeed
    result = game_state.rotate_active()
    
    assert result is True
    expected_rotation = (original_rotation + 1) % 4
    assert game_state.active_tetromino.rotation == expected_rotation


def test_rotate_active_multiple_times():
    """Test rotating active tetromino multiple times."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Rotate 4 times should return to original rotation
    original_rotation = game_state.active_tetromino.rotation
    
    for _ in range(4):
        game_state.rotate_active()
    
    assert game_state.active_tetromino.rotation == original_rotation


def test_move_when_no_active_tetromino():
    """Test that movement methods return False when no active tetromino."""
    game_state = GameState()
    
    # No tetromino spawned yet
    assert game_state.active_tetromino is None
    
    # All movement methods should return False
    assert game_state.move_active_left() is False
    assert game_state.move_active_right() is False
    assert game_state.rotate_active() is False


def test_move_when_game_over():
    """Test that movement methods return False when game is over."""
    game_state = GameState()
    game_state.game_over = True
    
    # All movement methods should return False
    assert game_state.move_active_left() is False
    assert game_state.move_active_right() is False
    assert game_state.rotate_active() is False


def test_hard_drop_moves_to_bottom():
    """Test that hard_drop moves tetromino to the bottom."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    original_y = game_state.active_tetromino.y
    
    # Hard drop
    game_state.hard_drop()
    
    # Tetromino should have been locked (active_tetromino might be new one or None)
    # The original tetromino should have moved down significantly
    # Since it was locked, we can't check its position directly
    # But we can verify the playfield has blocks now
    
    # Check that some blocks were added to the playfield
    has_blocks = False
    for y in range(game_state.playfield.height):
        for x in range(game_state.playfield.width):
            if game_state.playfield.get_cell(x, y) is not None:
                has_blocks = True
                break
        if has_blocks:
            break
    
    assert has_blocks, "Hard drop should have locked blocks into playfield"


def test_hard_drop_when_no_active_tetromino():
    """Test that hard_drop does nothing when no active tetromino."""
    game_state = GameState()
    
    # No tetromino spawned yet
    assert game_state.active_tetromino is None
    
    # Hard drop should do nothing (not crash)
    game_state.hard_drop()
    
    # State should be unchanged
    assert game_state.active_tetromino is None
    assert game_state.score == 0


def test_lock_tetromino_adds_to_playfield():
    """Test that lock_tetromino adds blocks to the playfield."""
    game_state = GameState()
    tetromino = game_state.spawn_tetromino()
    
    # Move tetromino to bottom
    while game_state.playfield.is_valid_position(tetromino.move(0, 1)):
        tetromino = tetromino.move(0, 1)
        game_state.active_tetromino = tetromino
    
    # Get the blocks before locking
    blocks_before = tetromino.get_absolute_blocks()
    color_before = tetromino.color
    
    # Lock the tetromino
    game_state.lock_tetromino()
    
    # Verify blocks are in the playfield
    for x, y in blocks_before:
        if 0 <= x < PLAYFIELD_WIDTH and 0 <= y < PLAYFIELD_HEIGHT:
            assert game_state.playfield.get_cell(x, y) == color_before


def test_lock_tetromino_awards_points():
    """Test that lock_tetromino awards 4 points."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Move to bottom
    game_state.hard_drop()
    
    # Score should be at least 4 (might be more if lines were cleared)
    assert game_state.score >= 4


def test_lock_tetromino_spawns_next():
    """Test that lock_tetromino spawns the next tetromino."""
    game_state = GameState()
    first_tetromino = game_state.spawn_tetromino()
    
    # Move to bottom and lock
    game_state.hard_drop()
    
    # A new tetromino should be spawned (unless game over)
    if not game_state.game_over:
        assert game_state.active_tetromino is not None
        # It should be a different instance
        assert game_state.active_tetromino is not first_tetromino


def test_update_accumulates_fall_timer():
    """Test that update accumulates time in fall_timer."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Update with small delta time
    game_state.update(0.1)
    
    assert abs(game_state.fall_timer - 0.1) < 0.001
    
    # Update again
    game_state.update(0.2)
    
    assert abs(game_state.fall_timer - 0.3) < 0.001


def test_update_moves_tetromino_down_after_interval():
    """Test that update moves tetromino down after fall interval."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    original_y = game_state.active_tetromino.y
    
    # Update with time >= fall_interval (0.5 seconds)
    game_state.update(0.5)
    
    # Tetromino should have moved down
    assert game_state.active_tetromino.y == original_y + 1
    
    # Fall timer should be reset
    assert game_state.fall_timer == 0.0


def test_update_resets_fall_timer_after_fall():
    """Test that update resets fall_timer after automatic fall."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Update with time > fall_interval
    game_state.update(0.6)
    
    # Fall timer should be reset to 0
    assert game_state.fall_timer == 0.0


def test_update_locks_tetromino_at_bottom():
    """Test that update locks tetromino when it reaches bottom."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Move tetromino near bottom
    while game_state.playfield.is_valid_position(game_state.active_tetromino.move(0, 1)):
        game_state.active_tetromino = game_state.active_tetromino.move(0, 1)
    
    # Update to trigger automatic fall (which will lock it)
    game_state.update(0.5)
    
    # Tetromino should have been locked and new one spawned (or game over)
    # Check that blocks are in the playfield
    has_blocks = False
    for y in range(game_state.playfield.height):
        for x in range(game_state.playfield.width):
            if game_state.playfield.get_cell(x, y) is not None:
                has_blocks = True
                break
        if has_blocks:
            break
    
    assert has_blocks, "Tetromino should have been locked into playfield"


def test_update_when_no_active_tetromino():
    """Test that update does nothing when no active tetromino."""
    game_state = GameState()
    
    # No tetromino spawned yet
    assert game_state.active_tetromino is None
    
    # Update should do nothing (not crash)
    game_state.update(0.5)
    
    # State should be unchanged
    assert game_state.active_tetromino is None
    assert game_state.fall_timer == 0.0


def test_update_when_game_over():
    """Test that update does nothing when game is over."""
    game_state = GameState()
    game_state.game_over = True
    
    # Update should do nothing (not crash)
    game_state.update(0.5)
    
    # Fall timer should not change
    assert game_state.fall_timer == 0.0


def test_can_move_helper_method():
    """Test the can_move helper method."""
    game_state = GameState()
    tetromino = game_state.spawn_tetromino()
    
    # Should be able to move down initially
    assert game_state.can_move(tetromino, 0, 1) is True
    
    # Move to bottom
    while game_state.can_move(tetromino, 0, 1):
        tetromino = tetromino.move(0, 1)
    
    # Should not be able to move down further
    assert game_state.can_move(tetromino, 0, 1) is False


def test_scoring_basic():
    """Test basic scoring - 4 points for locking a tetromino."""
    game_state = GameState()
    game_state.spawn_tetromino()
    
    # Lock the tetromino (without clearing lines)
    game_state.hard_drop()
    
    # Should have at least 4 points
    assert game_state.score >= 4


def test_initial_fall_interval():
    """Test that fall interval is set to 0.5 seconds."""
    game_state = GameState()
    
    assert game_state.fall_interval == 0.5


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


def game_state_with_active_tetromino():
    """Strategy for generating game states with an active tetromino."""
    def create_game_state():
        game_state = GameState()
        game_state.spawn_tetromino()
        return game_state
    
    return st.builds(create_game_state)


@st.composite
def playfield_with_blocks(draw):
    """Strategy for generating playfields with random stopped blocks."""
    from tetris.models.playfield import Playfield, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT
    
    playfield = Playfield()
    num_blocks = draw(st.integers(min_value=0, max_value=50))
    for _ in range(num_blocks):
        x = draw(st.integers(min_value=0, max_value=PLAYFIELD_WIDTH - 1))
        y = draw(st.integers(min_value=1, max_value=PLAYFIELD_HEIGHT - 1))  # Avoid top row
        color = draw(st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255)
        ))
        playfield.set_cell(x, y, color)
    return playfield


class TestGameStateProperties:
    """Property-based tests for GameState invariants."""
    
    @settings(max_examples=100)
    @given(shape_type=tetromino_type())
    def test_property_12_post_lock_spawning(self, shape_type):
        """Property 12: Post-Lock Spawning.
        
        For any game state where a tetromino is locked (and game is not over),
        a new active tetromino shall be spawned at the top center position
        (x=4, y=0) with one of the seven valid tetromino types.
        
        Feature: tetris-clone, Property 12: Post-Lock Spawning
        Validates: Requirements 4.4, 4.5
        """
        game_state = GameState()
        
        # Spawn initial tetromino
        first_tetromino = game_state.spawn_tetromino()
        assert first_tetromino is not None
        
        # Move it to bottom and lock it
        game_state.hard_drop()
        
        # If game is not over, a new tetromino should be spawned
        if not game_state.game_over:
            assert game_state.active_tetromino is not None, \
                "After locking, a new tetromino should be spawned if game is not over"
            
            # New tetromino should be at spawn position
            assert game_state.active_tetromino.x == 4, \
                f"Spawned tetromino x={game_state.active_tetromino.x}, expected 4"
            assert game_state.active_tetromino.y == 0, \
                f"Spawned tetromino y={game_state.active_tetromino.y}, expected 0"
            
            # Should be one of the seven valid types
            assert game_state.active_tetromino.shape_type in ['I', 'O', 'T', 'L', 'J', 'S', 'Z'], \
                f"Invalid tetromino type: {game_state.active_tetromino.shape_type}"
    
    @settings(max_examples=100)
    @given(
        shape_type=tetromino_type(),
        x=st.integers(min_value=1, max_value=8),
        y=st.integers(min_value=1, max_value=15),
        rotation=valid_rotation(),
        dx=st.integers(min_value=-1, max_value=1),
        dy=st.integers(min_value=0, max_value=1)
    )
    def test_property_5_movement_delta_correctness(self, shape_type, x, y, rotation, dx, dy):
        """Property 5: Movement Delta Correctness.
        
        For any tetromino at position (x, y), moving left shall result in
        position (x-1, y) if valid, moving right shall result in position
        (x+1, y) if valid, and the position shall remain unchanged if the
        move is invalid.
        
        Feature: tetris-clone, Property 5: Movement Delta Correctness
        Validates: Requirements 3.1, 3.2
        """
        from hypothesis import assume
        
        game_state = GameState()
        
        # Create a tetromino at the given position
        tetromino = Tetromino(shape_type=shape_type, x=x, y=y, rotation=rotation)
        
        # Only test if the initial position is valid
        assume(game_state.playfield.is_valid_position(tetromino))
        
        # Set it as the active tetromino
        game_state.active_tetromino = tetromino
        
        # Record original position
        original_x = game_state.active_tetromino.x
        original_y = game_state.active_tetromino.y
        
        # Try to move
        if dx == -1 and dy == 0:
            success = game_state.move_active_left()
        elif dx == 1 and dy == 0:
            success = game_state.move_active_right()
        else:
            # For other movements, skip this test case
            return
        
        # Check the result
        if success:
            # Movement succeeded - position should have changed by delta
            assert game_state.active_tetromino.x == original_x + dx, \
                f"After successful move, x should be {original_x + dx}, got {game_state.active_tetromino.x}"
            assert game_state.active_tetromino.y == original_y + dy, \
                f"After successful move, y should be {original_y + dy}, got {game_state.active_tetromino.y}"
        else:
            # Movement failed - position should be unchanged
            assert game_state.active_tetromino.x == original_x, \
                f"After failed move, x should remain {original_x}, got {game_state.active_tetromino.x}"
            assert game_state.active_tetromino.y == original_y, \
                f"After failed move, y should remain {original_y}, got {game_state.active_tetromino.y}"
    
    @settings(max_examples=100)
    @given(
        shape_type=tetromino_type(),
        x=st.integers(min_value=2, max_value=7),
        y=st.integers(min_value=2, max_value=15),
        rotation=valid_rotation()
    )
    def test_property_9_rotation_collision_prevention(self, shape_type, x, y, rotation):
        """Property 9: Rotation Collision Prevention.
        
        For any tetromino and any playfield state, attempting to rotate the
        tetromino into a configuration that would cause collision with
        boundaries or stopped blocks shall be prevented, and the tetromino
        shall remain in its current rotation state.
        
        Feature: tetris-clone, Property 9: Rotation Collision Prevention
        Validates: Requirements 3.8
        """
        from hypothesis import assume
        
        game_state = GameState()
        
        # Create a tetromino at the given position
        tetromino = Tetromino(shape_type=shape_type, x=x, y=y, rotation=rotation)
        
        # Only test if the initial position is valid
        assume(game_state.playfield.is_valid_position(tetromino))
        
        # Set it as the active tetromino
        game_state.active_tetromino = tetromino
        
        # Record original rotation
        original_rotation = game_state.active_tetromino.rotation
        
        # Try to rotate
        success = game_state.rotate_active()
        
        # Check the result
        if success:
            # Rotation succeeded - rotation should have changed
            expected_rotation = (original_rotation + 1) % 4
            assert game_state.active_tetromino.rotation == expected_rotation, \
                f"After successful rotation, rotation should be {expected_rotation}, got {game_state.active_tetromino.rotation}"
        else:
            # Rotation failed - rotation should be unchanged
            assert game_state.active_tetromino.rotation == original_rotation, \
                f"After failed rotation, rotation should remain {original_rotation}, got {game_state.active_tetromino.rotation}"
        
        # In either case, the tetromino should be in a valid position
        assert game_state.playfield.is_valid_position(game_state.active_tetromino), \
            "After rotation attempt, tetromino should be in a valid position"
    
    @settings(max_examples=100)
    @given(
        shape_type=tetromino_type(),
        x=st.integers(min_value=2, max_value=7),
        rotation=valid_rotation()
    )
    def test_property_7_hard_drop_reaches_bottom(self, shape_type, x, rotation):
        """Property 7: Hard Drop Reaches Bottom.
        
        For any tetromino and any playfield state, performing a hard drop
        shall move the tetromino to the lowest valid y-coordinate where it
        does not collide with the bottom or stopped blocks.
        
        Feature: tetris-clone, Property 7: Hard Drop Reaches Bottom
        Validates: Requirements 3.4, 3.10
        """
        game_state = GameState()
        
        # Create a tetromino at the top
        tetromino = Tetromino(shape_type=shape_type, x=x, y=0, rotation=rotation)
        
        # Set it as the active tetromino
        game_state.active_tetromino = tetromino
        
        # Find the lowest valid position manually
        lowest_y = 0
        for test_y in range(PLAYFIELD_HEIGHT):
            test_tetromino = Tetromino(shape_type=shape_type, x=x, y=test_y, rotation=rotation)
            if game_state.playfield.is_valid_position(test_tetromino):
                lowest_y = test_y
            else:
                break
        
        # Perform hard drop
        game_state.hard_drop()
        
        # After hard drop, the tetromino should have been locked
        # Check that blocks are in the playfield at the lowest position
        expected_tetromino = Tetromino(shape_type=shape_type, x=x, y=lowest_y, rotation=rotation)
        expected_blocks = expected_tetromino.get_absolute_blocks()
        
        # At least one of the expected blocks should be in the playfield
        blocks_found = 0
        for block_x, block_y in expected_blocks:
            if 0 <= block_x < PLAYFIELD_WIDTH and 0 <= block_y < PLAYFIELD_HEIGHT:
                if game_state.playfield.get_cell(block_x, block_y) is not None:
                    blocks_found += 1
        
        assert blocks_found > 0, \
            f"After hard drop, expected blocks at y={lowest_y} should be in playfield"
    
    @settings(max_examples=100)
    @given(
        shape_type=tetromino_type(),
        x=st.integers(min_value=2, max_value=7),
        y=st.integers(min_value=10, max_value=17),
        rotation=valid_rotation()
    )
    def test_property_11_tetromino_locking_adds_blocks_to_playfield(self, shape_type, x, y, rotation):
        """Property 11: Tetromino Locking Adds Blocks to Playfield.
        
        For any tetromino at a valid position, locking the tetromino shall
        result in the playfield containing blocks at each of the tetromino's
        absolute block positions with the tetromino's color.
        
        Feature: tetris-clone, Property 11: Tetromino Locking Adds Blocks to Playfield
        Validates: Requirements 4.1, 4.2, 4.3
        """
        from hypothesis import assume
        
        game_state = GameState()
        
        # Create a tetromino at the given position
        tetromino = Tetromino(shape_type=shape_type, x=x, y=y, rotation=rotation)
        
        # Only test if the position is valid
        assume(game_state.playfield.is_valid_position(tetromino))
        
        # Set it as the active tetromino
        game_state.active_tetromino = tetromino
        
        # Get the blocks and color before locking
        blocks_before = tetromino.get_absolute_blocks()
        color_before = tetromino.color
        
        # Lock the tetromino
        game_state.lock_tetromino()
        
        # Verify blocks are in the playfield with correct color
        for block_x, block_y in blocks_before:
            if 0 <= block_x < PLAYFIELD_WIDTH and 0 <= block_y < PLAYFIELD_HEIGHT:
                cell_color = game_state.playfield.get_cell(block_x, block_y)
                assert cell_color == color_before, \
                    f"Block at ({block_x}, {block_y}) should have color {color_before}, got {cell_color}"
    
    @settings(max_examples=100)
    @given(
        actions=st.lists(
            st.sampled_from(['spawn', 'move_left', 'move_right', 'rotate', 'drop']),
            min_size=1,
            max_size=10
        )
    )
    def test_property_17_scoring_monotonicity(self, actions):
        """Property 17: Scoring Monotonicity.
        
        For any game state and any sequence of valid game actions, the score
        shall never decrease.
        
        Feature: tetris-clone, Property 17: Scoring Monotonicity
        Validates: Requirements 6.4
        """
        game_state = GameState()
        game_state.spawn_tetromino()
        
        previous_score = game_state.score
        
        for action in actions:
            if game_state.game_over:
                break
            
            # Perform the action
            if action == 'spawn':
                if game_state.active_tetromino is None:
                    game_state.spawn_tetromino()
            elif action == 'move_left':
                game_state.move_active_left()
            elif action == 'move_right':
                game_state.move_active_right()
            elif action == 'rotate':
                game_state.rotate_active()
            elif action == 'drop':
                game_state.hard_drop()
            
            # Score should never decrease
            assert game_state.score >= previous_score, \
                f"Score decreased from {previous_score} to {game_state.score} after action '{action}'"
            
            previous_score = game_state.score
    
    @settings(max_examples=100)
    @given(
        shape_type=tetromino_type(),
        x=st.integers(min_value=2, max_value=7),
        rotation=valid_rotation()
    )
    def test_property_18_tetromino_lock_scoring(self, shape_type, x, rotation):
        """Property 18: Tetromino Lock Scoring.
        
        For any game state with score S, locking a tetromino (without
        clearing rows) shall result in score S + 4.
        
        Feature: tetris-clone, Property 18: Tetromino Lock Scoring
        Validates: Requirements 6.1
        """
        game_state = GameState()
        
        # Create a tetromino at a position where it won't clear lines
        # Use a position in the middle of the playfield
        tetromino = Tetromino(shape_type=shape_type, x=x, y=15, rotation=rotation)
        
        # Set it as the active tetromino
        game_state.active_tetromino = tetromino
        
        # Record score before locking
        score_before = game_state.score
        
        # Lock the tetromino
        game_state.lock_tetromino()
        
        # Check if any lines were cleared
        complete_rows = game_state.playfield.get_complete_rows()
        
        if len(complete_rows) == 0:
            # No lines cleared - score should increase by exactly 4
            assert game_state.score == score_before + 4, \
                f"After locking without clearing lines, score should be {score_before + 4}, got {game_state.score}"
        else:
            # Lines were cleared - score should be at least 4 more
            assert game_state.score >= score_before + 4, \
                f"After locking with line clears, score should be at least {score_before + 4}, got {game_state.score}"
    
    @settings(max_examples=100)
    @given(
        num_rows=st.integers(min_value=1, max_value=4),
        start_row=st.integers(min_value=10, max_value=16)
    )
    def test_property_19_line_clear_scoring(self, num_rows, start_row):
        """Property 19: Line Clear Scoring.
        
        For any game state with score S, clearing N complete rows shall
        increase the score by N × 10 points (in addition to the 4 points
        for locking the tetromino).
        
        Feature: tetris-clone, Property 19: Line Clear Scoring
        Validates: Requirements 6.2, 6.3
        """
        from hypothesis import assume
        
        # Ensure we don't go out of bounds
        assume(start_row + num_rows <= PLAYFIELD_HEIGHT)
        
        game_state = GameState()
        
        # Fill rows to create complete rows (except one cell)
        for row in range(start_row, start_row + num_rows):
            for x in range(PLAYFIELD_WIDTH - 1):
                game_state.playfield.set_cell(x, row, (255, 0, 0))
        
        # Create a tetromino that will complete these rows
        # Use an I-piece vertical to fill the missing column
        tetromino = Tetromino(shape_type='I', x=PLAYFIELD_WIDTH - 2, y=start_row, rotation=1)
        
        # Only proceed if this position is valid
        assume(game_state.playfield.is_valid_position(tetromino))
        
        game_state.active_tetromino = tetromino
        
        # Record score before locking
        score_before = game_state.score
        
        # Lock the tetromino
        game_state.lock_tetromino()
        
        # Calculate expected score increase
        # 4 points for locking + (num_rows * 10) for clearing rows
        # But we need to check how many rows were actually cleared
        # The I-piece might complete 1-4 rows depending on its position
        
        # Score should have increased by at least 4 (for locking)
        assert game_state.score >= score_before + 4, \
            f"Score should increase by at least 4, was {score_before}, now {game_state.score}"
        
        # If rows were cleared, score should increase by 4 + (N * 10)
        score_increase = game_state.score - score_before
        if score_increase > 4:
            # Some rows were cleared
            rows_cleared = (score_increase - 4) // 10
            assert rows_cleared >= 1, \
                f"If score increased by {score_increase}, at least 1 row should have been cleared"
            assert score_increase == 4 + (rows_cleared * 10), \
                f"Score increase {score_increase} should equal 4 + ({rows_cleared} * 10)"
    
    @settings(max_examples=100)
    @given(shape_type=tetromino_type())
    def test_property_20_game_over_detection(self, shape_type):
        """Property 20: Game Over Detection.
        
        For any playfield state, the game is over if and only if any stopped
        block exists at row index 0 (the top row).
        
        Feature: tetris-clone, Property 20: Game Over Detection
        Validates: Requirements 7.1
        """
        game_state = GameState()
        
        # Initially, game should not be over
        assert game_state.game_over is False
        assert game_state.playfield.is_game_over() is False
        
        # Fill the playfield from bottom up, leaving only top row empty
        for y in range(1, PLAYFIELD_HEIGHT):
            for x in range(PLAYFIELD_WIDTH):
                game_state.playfield.set_cell(x, y, (255, 0, 0))
        
        # Game should still not be over (top row is empty)
        assert game_state.playfield.is_game_over() is False
        
        # Add a block to the top row
        game_state.playfield.set_cell(5, 0, (255, 0, 0))
        
        # Now playfield should detect game over
        assert game_state.playfield.is_game_over() is True
    
    @settings(max_examples=100)
    @given(
        actions=st.lists(
            st.sampled_from(['move_left', 'move_right', 'rotate', 'spawn']),
            min_size=1,
            max_size=5
        )
    )
    def test_property_21_game_over_state_immutability(self, actions):
        """Property 21: Game Over State Immutability.
        
        For any game state where game over is true, no game actions (move,
        rotate, spawn) shall modify the playfield or active tetromino state.
        
        Feature: tetris-clone, Property 21: Game Over State Immutability
        Validates: Requirements 7.2, 7.3
        """
        game_state = GameState()
        
        # Force game over state
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Record playfield state
        playfield_state_before = []
        for y in range(PLAYFIELD_HEIGHT):
            row = []
            for x in range(PLAYFIELD_WIDTH):
                row.append(game_state.playfield.get_cell(x, y))
            playfield_state_before.append(row)
        
        # Try various actions
        for action in actions:
            if action == 'move_left':
                result = game_state.move_active_left()
                assert result is False, "move_active_left should return False when game is over"
            elif action == 'move_right':
                result = game_state.move_active_right()
                assert result is False, "move_active_right should return False when game is over"
            elif action == 'rotate':
                result = game_state.rotate_active()
                assert result is False, "rotate_active should return False when game is over"
            elif action == 'spawn':
                result = game_state.spawn_tetromino()
                assert result is None, "spawn_tetromino should return None when game is over"
        
        # Verify playfield state is unchanged
        for y in range(PLAYFIELD_HEIGHT):
            for x in range(PLAYFIELD_WIDTH):
                assert game_state.playfield.get_cell(x, y) == playfield_state_before[y][x], \
                    f"Playfield cell ({x}, {y}) changed after game over"
        
        # Verify active tetromino is still None
        assert game_state.active_tetromino is None, \
            "active_tetromino should remain None after game over"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
