"""Playfield module for Tetris clone.

This module defines the Playfield class which manages the 10×20 grid
where tetrominoes fall and accumulate. The playfield tracks the state
of each cell (empty or occupied with a color) and provides methods for
querying and modifying the grid state.
"""

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from tetris.models.tetromino import Tetromino

# Playfield dimensions constants
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20


class Playfield:
    """Manages the 10×20 grid state for the Tetris game.
    
    The playfield represents the playing area where tetrominoes fall and
    accumulate. Each cell in the grid can be either empty (None) or
    occupied by a block with a specific color (RGB tuple).
    
    Attributes:
        width: Number of columns in the playfield (always 10)
        height: Number of rows in the playfield (always 20)
        grid: 2D list representing the playfield state, where each cell
              is either None (empty) or an RGB color tuple (occupied)
    """
    
    def __init__(self) -> None:
        """Initialize a new empty playfield with 10×20 grid."""
        self.width = PLAYFIELD_WIDTH
        self.height = PLAYFIELD_HEIGHT
        # Initialize grid as 20 rows × 10 columns with None values
        # grid[y][x] where y is row (0=top, 19=bottom) and x is column (0=left, 9=right)
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def get_cell(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get the color value at the specified grid position.
        
        Args:
            x: Column index (0-9)
            y: Row index (0-19)
        
        Returns:
            None if the cell is empty, or an RGB color tuple if occupied
        
        Raises:
            IndexError: If x or y are out of bounds
        """
        if not (0 <= x < self.width):
            raise IndexError(f"Column index {x} out of bounds (0-{self.width-1})")
        if not (0 <= y < self.height):
            raise IndexError(f"Row index {y} out of bounds (0-{self.height-1})")
        
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, color: Optional[Tuple[int, int, int]]) -> None:
        """Set the color value at the specified grid position.
        
        Args:
            x: Column index (0-9)
            y: Row index (0-19)
            color: RGB color tuple to set, or None to clear the cell
        
        Raises:
            IndexError: If x or y are out of bounds
        """
        if not (0 <= x < self.width):
            raise IndexError(f"Column index {x} out of bounds (0-{self.width-1})")
        if not (0 <= y < self.height):
            raise IndexError(f"Row index {y} out of bounds (0-{self.height-1})")
        
        self.grid[y][x] = color
    
    def is_valid_position(self, tetromino: 'Tetromino') -> bool:
        """Check if a tetromino position is valid (no collisions).
        
        A position is valid if all blocks of the tetromino:
        1. Are within the playfield boundaries (0 <= x < 10, 0 <= y < 20)
        2. Do not overlap with any stopped blocks in the grid
        
        Args:
            tetromino: The tetromino to check
        
        Returns:
            True if the position is valid, False otherwise
        """
        blocks = tetromino.get_absolute_blocks()
        
        for x, y in blocks:
            # Check boundary collisions
            if x < 0 or x >= self.width:
                return False
            if y < 0 or y >= self.height:
                return False
            
            # Check collision with stopped blocks
            if self.grid[y][x] is not None:
                return False
        
        return True
    
    def add_tetromino(self, tetromino: 'Tetromino') -> None:
        """Lock a tetromino into the playfield by adding its blocks to the grid.
        
        This method converts an active (falling) tetromino into stopped blocks
        by setting each of the tetromino's block positions in the grid to the
        tetromino's color. This is called when a tetromino lands and can no
        longer move down.
        
        Args:
            tetromino: The tetromino to lock into the playfield
        
        Side effects:
            Modifies the grid by setting cells to the tetromino's color
        """
        blocks = tetromino.get_absolute_blocks()
        color = tetromino.color
        
        for x, y in blocks:
            # Set each block position to the tetromino's color
            # Note: We assume the tetromino is in a valid position
            # (this should be verified by the caller before locking)
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = color
    
    def get_complete_rows(self) -> list[int]:
        """Find all rows that are completely filled with blocks.
        
        A row is complete when all 10 positions in that row contain
        non-None color values (i.e., all cells are occupied).
        
        Returns:
            List of row indices (0-19) that are complete, in ascending order
        """
        complete_rows = []
        
        for y in range(self.height):
            # Check if all cells in this row are occupied
            if all(self.grid[y][x] is not None for x in range(self.width)):
                complete_rows.append(y)
        
        return complete_rows
    
    def clear_rows(self, row_indices: list[int]) -> None:
        """Clear specified rows and shift blocks above them down.
        
        This method removes the specified rows from the playfield and moves
        all rows above each cleared row down by one position. The process
        preserves the color and position of blocks when moving rows downward.
        
        When multiple rows are cleared, they are processed from bottom to top
        to ensure correct gravity behavior.
        
        Args:
            row_indices: List of row indices to clear (can be in any order)
        
        Side effects:
            Modifies the grid by removing rows and shifting blocks down
        """
        if not row_indices:
            return
        
        # Sort row indices in ascending order to process from top to bottom
        sorted_rows = sorted(set(row_indices))
        
        # Remove all the specified rows
        for row_index in reversed(sorted_rows):
            del self.grid[row_index]
        
        # Add empty rows at the top to maintain grid size
        num_cleared = len(sorted_rows)
        for _ in range(num_cleared):
            self.grid.insert(0, [None for _ in range(self.width)])
    
    def is_game_over(self) -> bool:
        """Check if the game is over by detecting blocks in the top row.
        
        The game is over when any stopped block exists in the top row (y=0)
        of the playfield. This indicates that the playfield has filled up
        and there is no room for new tetrominoes to spawn.
        
        Returns:
            True if any block exists in the top row, False otherwise
        """
        # Check if any cell in the top row (y=0) is occupied
        return any(self.grid[0][x] is not None for x in range(self.width))
