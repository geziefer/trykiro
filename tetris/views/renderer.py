"""Renderer module for Tetris clone.

This module defines the Renderer class which handles all Pygame-based
graphics rendering. The renderer is responsible for drawing the playfield,
tetrominoes, score, and other visual elements to the screen.
"""

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from tetris.models.game_state import GameState
    from tetris.models.playfield import Playfield
    from tetris.models.tetromino import Tetromino


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Block size (each grid cell is 30x30 pixels)
BLOCK_SIZE = 30

# Playfield dimensions (from models)
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20

# Playfield offset (centered horizontally, 50 pixels from top)
PLAYFIELD_OFFSET_X = (SCREEN_WIDTH - PLAYFIELD_WIDTH * BLOCK_SIZE) // 2
PLAYFIELD_OFFSET_Y = 50

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
BACKGROUND_COLOR = (20, 20, 20)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)


class Renderer:
    """Handles all Pygame-based graphics rendering.
    
    The Renderer class is responsible for drawing the game state to the screen.
    It reads from the game state but never modifies it (view layer principle).
    
    Attributes:
        screen: Pygame surface to draw on
        block_size: Size of each grid cell in pixels
        offset_x: Horizontal offset of playfield from screen edge
        offset_y: Vertical offset of playfield from screen edge
        title_font: Large font for titles
        score_font: Medium font for score display
        text_font: Small font for general text
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the renderer with a Pygame surface.
        
        Args:
            screen: Pygame surface to draw on (typically from pygame.display.set_mode)
        """
        self.screen = screen
        self.block_size = BLOCK_SIZE
        self.offset_x = PLAYFIELD_OFFSET_X
        self.offset_y = PLAYFIELD_OFFSET_Y
        
        # Initialize fonts (load once and reuse)
        self.title_font = pygame.font.Font(None, 72)   # Large for title
        self.score_font = pygame.font.Font(None, 36)   # Medium for score
        self.text_font = pygame.font.Font(None, 24)    # Small for text
    
    def grid_to_screen(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        """Convert grid coordinates to screen pixel coordinates.
        
        Args:
            grid_x: Grid column (0-9)
            grid_y: Grid row (0-19)
        
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        screen_x = self.offset_x + grid_x * self.block_size
        screen_y = self.offset_y + grid_y * self.block_size
        return screen_x, screen_y
    
    def draw_text(self, text: str, font: pygame.font.Font,
                  color: tuple[int, int, int], x: int, y: int,
                  center: bool = False) -> None:
        """Draw text at specified position.
        
        Args:
            text: Text string to render
            font: Pygame font to use
            color: RGB color tuple
            x: X coordinate
            y: Y coordinate
            center: If True, center text at (x, y); if False, use (x, y) as top-left
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        
        self.screen.blit(text_surface, text_rect)

    def draw_block(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        """Draw a single block at grid position (x, y).
        
        Args:
            x: Grid column (0-9)
            y: Grid row (0-19)
            color: RGB color tuple for the block
        """
        screen_x, screen_y = self.grid_to_screen(x, y)
        
        # Draw filled rectangle for the block
        rect = pygame.Rect(screen_x, screen_y, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw border for visual separation
        pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def render_grid_lines(self) -> None:
        """Draw playfield border and grid lines.
        
        Draws a white border around the playfield to clearly delineate
        the game boundaries.
        """
        # Calculate border rectangle
        border_rect = pygame.Rect(
            self.offset_x - 2,
            self.offset_y - 2,
            PLAYFIELD_WIDTH * self.block_size + 4,
            PLAYFIELD_HEIGHT * self.block_size + 4
        )
        
        # Draw white border (2 pixels thick)
        pygame.draw.rect(self.screen, WHITE, border_rect, 2)
    
    def render_playfield(self, playfield: 'Playfield') -> None:
        """Draw all stopped blocks in the playfield.
        
        Iterates through the playfield grid and draws each occupied cell
        with its assigned color.
        
        Args:
            playfield: The Playfield instance to render
        """
        # Draw each occupied cell in the grid
        for y in range(PLAYFIELD_HEIGHT):
            for x in range(PLAYFIELD_WIDTH):
                cell_color = playfield.get_cell(x, y)
                if cell_color is not None:
                    # Cell is occupied - draw the block
                    self.draw_block(x, y, cell_color)

    def render_tetromino(self, tetromino: 'Tetromino') -> None:
        """Draw the active tetromino.
        
        Draws all blocks of the tetromino using its color.
        
        Args:
            tetromino: The Tetromino instance to render
        """
        # Get absolute block positions
        blocks = tetromino.get_absolute_blocks()
        color = tetromino.color
        
        # Draw each block
        for x, y in blocks:
            # Only draw blocks that are within the visible playfield
            if 0 <= x < PLAYFIELD_WIDTH and 0 <= y < PLAYFIELD_HEIGHT:
                self.draw_block(x, y, color)

    def render_score(self, score: int) -> None:
        """Display the current score at the top of the screen.
        
        Args:
            score: The current score value to display
        """
        score_text = f"Score: {score}"
        # Draw score at top center of screen
        self.draw_text(
            score_text,
            self.score_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            20,
            center=True
        )

    def render_game(self, game_state: 'GameState') -> None:
        """Render the complete game screen.
        
        This is the main rendering method that coordinates all rendering
        operations. It follows the proper rendering order:
        1. Clear screen
        2. Draw grid lines
        3. Draw playfield (stopped blocks)
        4. Draw active tetromino
        5. Draw score
        
        Args:
            game_state: The GameState instance to render
        
        Side effects:
            Draws to the screen surface (does not call pygame.display.flip)
        """
        # 1. Clear screen with background color
        self.screen.fill(BACKGROUND_COLOR)
        
        # 2. Draw playfield border
        self.render_grid_lines()
        
        # 3. Draw stopped blocks from playfield
        self.render_playfield(game_state.playfield)
        
        # 4. Draw active tetromino (if it exists)
        if game_state.active_tetromino is not None:
            self.render_tetromino(game_state.active_tetromino)
        
        # 5. Draw score
        self.render_score(game_state.score)
        
        # Note: pygame.display.flip() should be called by the main loop,
        # not by the renderer
