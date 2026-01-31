"""Tetromino shapes and rotation logic.

This module defines the seven classic Tetris tetromino shapes (I, O, T, L, J, S, Z)
with their rotation states, colors, and movement operations. All operations are
immutable - they return new Tetromino instances rather than modifying existing ones.
"""

from typing import List, Tuple

# Type aliases for clarity
Position = Tuple[int, int]
Color = Tuple[int, int, int]
BlockList = List[Position]


# Color constants for each tetromino type
TETROMINO_COLORS = {
    'I': (0, 255, 255),      # Cyan
    'O': (255, 255, 0),      # Yellow
    'T': (128, 0, 128),      # Purple
    'L': (255, 165, 0),      # Orange
    'J': (0, 0, 255),        # Dark Blue
    'S': (0, 255, 0),        # Green
    'Z': (255, 0, 0),        # Red
}


# Shape definitions: each shape has 4 rotation states
# Each rotation state is a list of (x, y) offsets from the center position
# Coordinates are relative to a center point, with positive x to the right and positive y down

TETROMINO_SHAPES = {
    'I': [
        # Rotation 0: Horizontal
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        # Rotation 1: Vertical
        [(1, 0), (1, 1), (1, 2), (1, 3)],
        # Rotation 2: Horizontal (same as 0)
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        # Rotation 3: Vertical (same as 1)
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    'O': [
        # Rotation 0-3: Square (all the same)
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    'T': [
        # Rotation 0: T pointing up
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        # Rotation 1: T pointing right
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        # Rotation 2: T pointing down
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        # Rotation 3: T pointing left
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'L': [
        # Rotation 0: L with base at bottom, extending right
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        # Rotation 1: L rotated 90° clockwise
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        # Rotation 2: L rotated 180°
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        # Rotation 3: L rotated 270°
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
    'J': [
        # Rotation 0: J with base at bottom, extending left
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        # Rotation 1: J rotated 90° clockwise
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        # Rotation 2: J rotated 180°
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        # Rotation 3: J rotated 270°
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    'S': [
        # Rotation 0: S horizontal
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        # Rotation 1: S vertical
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        # Rotation 2: S horizontal (same as 0)
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        # Rotation 3: S vertical (same as 1)
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    'Z': [
        # Rotation 0: Z horizontal
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        # Rotation 1: Z vertical
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        # Rotation 2: Z horizontal (same as 0)
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        # Rotation 3: Z vertical (same as 1)
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
}


class Tetromino:
    """Represents a tetromino piece with shape, color, position, and rotation.
    
    Tetrominoes are immutable - all operations (move, rotate) return new instances
    rather than modifying the existing instance. This makes the code easier to reason
    about and safer for testing.
    
    Attributes:
        shape_type: One of 'I', 'O', 'T', 'L', 'J', 'S', 'Z'
        x: Grid x-coordinate (column) of the tetromino's center
        y: Grid y-coordinate (row) of the tetromino's center
        rotation: Rotation state (0, 1, 2, or 3 representing 0°, 90°, 180°, 270°)
        color: RGB color tuple for rendering
    """
    
    def __init__(self, shape_type: str, x: int, y: int, rotation: int = 0):
        """Initialize a tetromino with the given shape, position, and rotation.
        
        Args:
            shape_type: One of 'I', 'O', 'T', 'L', 'J', 'S', 'Z'
            x: Grid x-coordinate (column)
            y: Grid y-coordinate (row)
            rotation: Rotation state (0-3), defaults to 0
            
        Raises:
            ValueError: If shape_type is not one of the seven valid types
            ValueError: If rotation is not in range 0-3
        """
        if shape_type not in TETROMINO_SHAPES:
            raise ValueError(
                f"Invalid shape_type '{shape_type}'. "
                f"Must be one of: {', '.join(TETROMINO_SHAPES.keys())}"
            )
        
        if rotation not in (0, 1, 2, 3):
            raise ValueError(f"Invalid rotation {rotation}. Must be 0, 1, 2, or 3")
        
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.rotation = rotation
        self.color = TETROMINO_COLORS[shape_type]
    
    def get_blocks(self) -> BlockList:
        """Get the relative block positions for the current rotation state.
        
        Returns:
            List of (x, y) tuples representing block positions relative to center
        """
        return TETROMINO_SHAPES[self.shape_type][self.rotation]
    
    def get_absolute_blocks(self) -> BlockList:
        """Get the absolute grid positions of all blocks.
        
        Calculates the actual grid coordinates by adding the tetromino's position
        to each relative block offset.
        
        Returns:
            List of (x, y) tuples representing absolute grid positions
        """
        blocks = self.get_blocks()
        return [(self.x + bx, self.y + by) for bx, by in blocks]
    
    def move(self, dx: int, dy: int) -> 'Tetromino':
        """Return a new tetromino moved by the given offset.
        
        This is an immutable operation - it returns a new Tetromino instance
        rather than modifying the current one.
        
        Args:
            dx: Horizontal offset (positive = right, negative = left)
            dy: Vertical offset (positive = down, negative = up)
            
        Returns:
            New Tetromino instance at the moved position
        """
        return Tetromino(
            shape_type=self.shape_type,
            x=self.x + dx,
            y=self.y + dy,
            rotation=self.rotation
        )
    
    def rotate_clockwise(self) -> 'Tetromino':
        """Return a new tetromino rotated 90 degrees clockwise.
        
        This is an immutable operation - it returns a new Tetromino instance
        rather than modifying the current one. The center position (x, y) is
        preserved during rotation.
        
        Returns:
            New Tetromino instance with rotation incremented by 1 (mod 4)
        """
        new_rotation = (self.rotation + 1) % 4
        return Tetromino(
            shape_type=self.shape_type,
            x=self.x,
            y=self.y,
            rotation=new_rotation
        )
    
    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return (
            f"Tetromino(shape_type='{self.shape_type}', "
            f"x={self.x}, y={self.y}, rotation={self.rotation})"
        )
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on shape, position, and rotation."""
        if not isinstance(other, Tetromino):
            return NotImplemented
        return (
            self.shape_type == other.shape_type
            and self.x == other.x
            and self.y == other.y
            and self.rotation == other.rotation
        )
