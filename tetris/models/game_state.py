"""GameState module for Tetris clone.

This module defines the GameState class which coordinates all game logic
and rules. It manages the playfield, active tetromino, score, game over
state, and automatic falling mechanics.
"""

import random
from typing import Optional

from tetris.models.playfield import Playfield
from tetris.models.tetromino import Tetromino


# Game timing constants
DEFAULT_FALL_INTERVAL = 0.5  # Seconds between automatic falls


class GameState:
    """Central game state manager coordinating all game logic and rules.
    
    The GameState class is responsible for:
    - Managing the playfield and active tetromino
    - Handling player input (move, rotate, drop)
    - Implementing automatic falling mechanics
    - Scoring and game over detection
    - Spawning new tetrominoes
    
    Attributes:
        playfield: The 10×20 game grid
        active_tetromino: Currently falling piece (None if game over)
        score: Current player score
        game_over: Whether the game has ended
        fall_timer: Time accumulator for automatic falling (seconds)
        fall_interval: Time between automatic falls (seconds)
    """
    
    def __init__(self) -> None:
        """Initialize a new game state with empty playfield.
        
        Creates an empty playfield, sets score to 0, and initializes
        the fall timer. No tetromino is spawned initially - the caller
        should call spawn_tetromino() to start the game.
        """
        self.playfield = Playfield()
        self.active_tetromino: Optional[Tetromino] = None
        self.score = 0
        self.game_over = False
        
        # Fall timing
        self.fall_timer = 0.0
        self.fall_interval = DEFAULT_FALL_INTERVAL
    
    def reset(self) -> None:
        """Reset the game state to start a new game.
        
        Clears the playfield, resets score to 0, clears game over flag,
        and resets the fall timer. Does not spawn a new tetromino - the
        caller should call spawn_tetromino() after reset.
        
        Side effects:
            - Creates new empty playfield
            - Resets score to 0
            - Clears game_over flag
            - Clears active_tetromino
            - Resets fall_timer
        """
        self.playfield = Playfield()
        self.active_tetromino = None
        self.score = 0
        self.game_over = False
        self.fall_timer = 0.0
    
    def spawn_tetromino(self) -> Optional[Tetromino]:
        """Spawn a new random tetromino at the top center of the playfield.
        
        Randomly selects one of the seven tetromino types and creates it
        at position (x=4, y=0) with rotation 0. If the spawn position is
        already occupied (collision), triggers game over.
        
        Returns:
            The newly spawned tetromino, or None if game over
        
        Side effects:
            - Sets self.active_tetromino to the new tetromino
            - May set self.game_over to True if spawn collision occurs
        """
        # Don't spawn if game is already over
        if self.game_over:
            return None
        
        # Randomly select a tetromino type
        shape_types = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        shape_type = random.choice(shape_types)
        
        # Create tetromino at top center (x=4, y=0)
        new_tetromino = Tetromino(shape_type=shape_type, x=4, y=0, rotation=0)
        
        # Check if spawn position is valid
        if not self.playfield.is_valid_position(new_tetromino):
            # Spawn collision - game over
            self.game_over = True
            self.active_tetromino = None
            return None
        
        self.active_tetromino = new_tetromino
        return new_tetromino
    
    def move_active_left(self) -> bool:
        """Attempt to move the active tetromino one column left.
        
        Validates the move using playfield collision detection. Only
        updates the active tetromino if the move is valid.
        
        Returns:
            True if the move was successful, False otherwise
        """
        if self.active_tetromino is None or self.game_over:
            return False
        
        # Try moving left
        moved = self.active_tetromino.move(-1, 0)
        
        # Check if the new position is valid
        if self.playfield.is_valid_position(moved):
            self.active_tetromino = moved
            return True
        
        return False
    
    def move_active_right(self) -> bool:
        """Attempt to move the active tetromino one column right.
        
        Validates the move using playfield collision detection. Only
        updates the active tetromino if the move is valid.
        
        Returns:
            True if the move was successful, False otherwise
        """
        if self.active_tetromino is None or self.game_over:
            return False
        
        # Try moving right
        moved = self.active_tetromino.move(1, 0)
        
        # Check if the new position is valid
        if self.playfield.is_valid_position(moved):
            self.active_tetromino = moved
            return True
        
        return False
    
    def rotate_active(self) -> bool:
        """Attempt to rotate the active tetromino 90 degrees clockwise.
        
        Validates the rotation using playfield collision detection. Only
        updates the active tetromino if the rotation is valid.
        
        Returns:
            True if the rotation was successful, False otherwise
        """
        if self.active_tetromino is None or self.game_over:
            return False
        
        # Try rotating clockwise
        rotated = self.active_tetromino.rotate_clockwise()
        
        # Check if the new rotation is valid
        if self.playfield.is_valid_position(rotated):
            self.active_tetromino = rotated
            return True
        
        return False
    
    def hard_drop(self) -> None:
        """Drop the active tetromino to the bottom and lock it immediately.
        
        Moves the active tetromino down until it collides with the bottom
        or stopped blocks, then immediately locks it into the playfield.
        
        Side effects:
            - Moves active tetromino to lowest valid position
            - Calls lock_tetromino() to finalize the placement
        """
        if self.active_tetromino is None or self.game_over:
            return
        
        # Move down until collision
        while True:
            moved = self.active_tetromino.move(0, 1)
            if self.playfield.is_valid_position(moved):
                self.active_tetromino = moved
            else:
                # Can't move down further - lock it
                break
        
        # Lock the tetromino at its final position
        self.lock_tetromino()
    
    def lock_tetromino(self) -> None:
        """Lock the active tetromino into the playfield and handle consequences.
        
        This method:
        1. Adds the active tetromino's blocks to the playfield
        2. Awards 4 points for locking the tetromino
        3. Checks for complete rows and clears them
        4. Awards 10 points per cleared row
        5. Checks for game over condition
        6. Spawns the next tetromino (if game not over)
        
        Side effects:
            - Modifies playfield grid
            - Updates score
            - May set game_over to True
            - Spawns new active tetromino or sets it to None
        """
        if self.active_tetromino is None or self.game_over:
            return
        
        # Add tetromino blocks to playfield
        self.playfield.add_tetromino(self.active_tetromino)
        
        # Award points for locking (4 points)
        self.score += 4
        
        # Check for complete rows
        complete_rows = self.playfield.get_complete_rows()
        
        # Clear complete rows and award bonus points
        if complete_rows:
            self.playfield.clear_rows(complete_rows)
            # Award 10 points per cleared row
            self.score += len(complete_rows) * 10
        
        # Check for game over (blocks in top row)
        if self.playfield.is_game_over():
            self.game_over = True
            self.active_tetromino = None
            return
        
        # Spawn next tetromino
        self.spawn_tetromino()
    
    def update(self, delta_time: float) -> None:
        """Update game state for automatic falling mechanics.
        
        Accumulates time in the fall timer. When the fall interval is
        reached, moves the active tetromino down one row. If it can't
        move down, locks it into the playfield.
        
        Args:
            delta_time: Time elapsed since last update (in seconds)
        
        Side effects:
            - Updates fall_timer
            - May move active tetromino down
            - May lock tetromino and spawn next one
        """
        if self.active_tetromino is None or self.game_over:
            return
        
        # Accumulate time
        self.fall_timer += delta_time
        
        # Check if it's time to fall
        if self.fall_timer >= self.fall_interval:
            # Reset timer
            self.fall_timer = 0.0
            
            # Try to move down
            moved = self.active_tetromino.move(0, 1)
            
            if self.playfield.is_valid_position(moved):
                # Move down successful
                self.active_tetromino = moved
            else:
                # Can't move down - lock the tetromino
                self.lock_tetromino()
    
    def can_move(self, tetromino: Tetromino, dx: int, dy: int) -> bool:
        """Check if a tetromino can move by the given offset.
        
        This is a helper method for testing and validation.
        
        Args:
            tetromino: The tetromino to check
            dx: Horizontal offset
            dy: Vertical offset
        
        Returns:
            True if the move is valid, False otherwise
        """
        moved = tetromino.move(dx, dy)
        return self.playfield.is_valid_position(moved)
