"""UI screen management for Tetris clone.

This module defines the UIManager class which manages different game screens
and transitions between them (start screen, game screen, game over screen,
name entry screen, high scores screen).
"""

from enum import Enum, auto
from typing import TYPE_CHECKING, Optional, List

import pygame

if TYPE_CHECKING:
    from tetris.models.high_scores import HighScoreEntry


# Screen dimensions (must match renderer)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Color constants
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 0)


class Screen(Enum):
    """Enumeration of all possible game screens."""
    START = auto()
    GAME = auto()
    GAME_OVER = auto()
    NAME_ENTRY = auto()
    HIGH_SCORES = auto()


class UIManager:
    """Manages UI screens and transitions.
    
    The UIManager is responsible for rendering different screens (start, game,
    game over, name entry, high scores) and handling transitions between them.
    
    Attributes:
        current_screen: The currently active screen
        screen: Pygame surface to draw on
        title_font: Large font for titles
        score_font: Medium font for scores
        text_font: Small font for general text
        player_name: Current name being entered (for name entry screen)
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the UI manager.
        
        Args:
            screen: Pygame surface to draw on
        """
        self.current_screen = Screen.START
        self.screen = screen
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 72)   # Large for titles
        self.score_font = pygame.font.Font(None, 48)   # Medium for scores
        self.text_font = pygame.font.Font(None, 32)    # Small for text
        
        # Name entry state
        self.player_name = ""
    
    def transition_to(self, screen: Screen) -> None:
        """Transition to a different screen.
        
        Args:
            screen: The screen to transition to
        """
        self.current_screen = screen
        
        # Reset state when transitioning to name entry
        if screen == Screen.NAME_ENTRY:
            self.player_name = ""
    
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
    
    def render_start_screen(self) -> None:
        """Render the start screen.
        
        Displays the game title and instructions to start.
        """
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        self.draw_text(
            "TETRIS",
            self.title_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            center=True
        )
        
        # Draw start prompt
        self.draw_text(
            "Press SPACE to start",
            self.text_font,
            HIGHLIGHT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            center=True
        )
    
    def render_game_over_screen(self, final_score: int) -> None:
        """Render the game over screen.
        
        Displays "GAME OVER" message and the final score.
        
        Args:
            final_score: The player's final score
        """
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw "GAME OVER" title
        self.draw_text(
            "GAME OVER",
            self.title_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            center=True
        )
        
        # Draw final score
        score_text = f"Final Score: {final_score}"
        self.draw_text(
            score_text,
            self.score_font,
            HIGHLIGHT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            center=True
        )
        
        # Draw continue prompt
        self.draw_text(
            "Press SPACE to continue",
            self.text_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 2 // 3,
            center=True
        )
    
    def render_name_entry_screen(self, score: int) -> None:
        """Render the name entry screen for high scores.
        
        Displays "New High Score!" message, the score, and a text input
        field for entering the player's name.
        
        Args:
            score: The high score achieved
        """
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw "New High Score!" title
        self.draw_text(
            "New High Score!",
            self.title_font,
            HIGHLIGHT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 4,
            center=True
        )
        
        # Draw score
        score_text = f"Score: {score}"
        self.draw_text(
            score_text,
            self.score_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 3,
            center=True
        )
        
        # Draw name entry prompt
        self.draw_text(
            "Enter your name:",
            self.text_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 40,
            center=True
        )
        
        # Draw current name (with cursor)
        name_display = self.player_name + "_"
        self.draw_text(
            name_display,
            self.score_font,
            HIGHLIGHT_COLOR,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 20,
            center=True
        )
        
        # Draw submit prompt
        self.draw_text(
            "Press ENTER to submit",
            self.text_font,
            GRAY,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 2 // 3,
            center=True
        )
    
    def render_high_scores_screen(self, high_scores: List['HighScoreEntry']) -> None:
        """Render the high scores display screen.
        
        Displays the top 10 high scores with player names in descending order.
        
        Args:
            high_scores: List of high score entries to display
        """
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        self.draw_text(
            "HIGH SCORES",
            self.title_font,
            TEXT_COLOR,
            SCREEN_WIDTH // 2,
            80,
            center=True
        )
        
        # Draw high scores list
        start_y = 180
        line_height = 35
        
        if not high_scores:
            # No high scores yet
            self.draw_text(
                "No high scores yet!",
                self.text_font,
                GRAY,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                center=True
            )
        else:
            for i, entry in enumerate(high_scores[:10]):  # Top 10 only
                # Format: "1. ALICE .......... 1000"
                rank = f"{i + 1}."
                name = entry.name[:15]  # Limit name length
                score = str(entry.score)
                
                # Draw rank and name (left-aligned)
                rank_name = f"{rank:3} {name}"
                self.draw_text(
                    rank_name,
                    self.text_font,
                    TEXT_COLOR,
                    SCREEN_WIDTH // 2 - 150,
                    start_y + i * line_height,
                    center=False
                )
                
                # Draw score (right-aligned)
                self.draw_text(
                    score,
                    self.text_font,
                    HIGHLIGHT_COLOR,
                    SCREEN_WIDTH // 2 + 150,
                    start_y + i * line_height,
                    center=False
                )
        
        # Draw return prompt
        self.draw_text(
            "Press SPACE to return",
            self.text_font,
            GRAY,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 60,
            center=True
        )
    
    def handle_name_entry_input(self, event: pygame.event.Event) -> None:
        """Handle text input for name entry.
        
        Processes keyboard events to build the player name string.
        Handles character input, backspace, and enter.
        
        Args:
            event: Pygame keyboard event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Submit is handled by the caller
                pass
            elif event.key == pygame.K_SPACE:
                # Add space (limit name length)
                if len(self.player_name) < 20:
                    self.player_name += " "
            else:
                # Add character (limit name length)
                if len(self.player_name) < 20:
                    char = event.unicode
                    # Only allow printable characters
                    if char.isprintable() and char not in ['\r', '\n', '\t']:
                        self.player_name += char
