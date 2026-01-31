"""Input handling for Tetris clone.

This module defines the InputHandler class which processes keyboard events
and translates them into game actions. The input handler is a thin routing
layer that doesn't contain business logic.
"""

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from tetris.models.game_state import GameState
    from tetris.views.ui_screens import UIManager, Screen


class InputHandler:
    """Handles keyboard input and routes to appropriate game actions.
    
    The InputHandler is a thin controller layer that translates Pygame
    keyboard events into method calls on the game state or UI manager.
    It contains no business logic - just routing.
    
    The handler supports three types of input:
    - Game input: Controls during active gameplay (move, rotate, drop)
    - Menu input: Navigation in menu screens (start game, view scores)
    - Text input: Character entry for player names
    """
    
    def __init__(self) -> None:
        """Initialize the input handler."""
        pass
    
    def handle_game_input(self, event: pygame.event.Event,
                         game_state: 'GameState') -> None:
        """Handle keyboard input during active gameplay.
        
        Maps keyboard events to game state methods:
        - LEFT ARROW: Move active tetromino left
        - RIGHT ARROW: Move active tetromino right
        - SPACE: Rotate active tetromino clockwise
        - DOWN ARROW: Hard drop (drop to bottom immediately)
        
        Args:
            event: Pygame keyboard event (must be KEYDOWN type)
            game_state: The GameState instance to control
        """
        if event.type != pygame.KEYDOWN:
            return
        
        if event.key == pygame.K_LEFT:
            game_state.move_active_left()
        elif event.key == pygame.K_RIGHT:
            game_state.move_active_right()
        elif event.key == pygame.K_SPACE:
            game_state.rotate_active()
        elif event.key == pygame.K_DOWN:
            game_state.hard_drop()
    
    def handle_menu_input(self, event: pygame.event.Event,
                         ui_manager: 'UIManager',
                         game_state: 'GameState') -> None:
        """Handle keyboard input in menu screens.
        
        Handles navigation and actions in non-gameplay screens:
        - START screen: SPACE starts the game
        - GAME_OVER screen: SPACE continues to high scores or name entry
        - HIGH_SCORES screen: SPACE returns to start screen
        
        Args:
            event: Pygame keyboard event (must be KEYDOWN type)
            ui_manager: The UIManager instance to control screen transitions
            game_state: The GameState instance (for starting new games)
        """
        if event.type != pygame.KEYDOWN:
            return
        
        # Import Screen enum here to avoid circular imports
        from tetris.views.ui_screens import Screen
        
        if event.key == pygame.K_SPACE:
            if ui_manager.current_screen == Screen.START:
                # Start a new game
                game_state.reset()
                game_state.spawn_tetromino()
                ui_manager.transition_to(Screen.GAME)
            
            elif ui_manager.current_screen == Screen.GAME_OVER:
                # Continue to high scores or name entry
                # (Caller should check if score qualifies for high score list)
                pass
            
            elif ui_manager.current_screen == Screen.HIGH_SCORES:
                # Return to start screen
                ui_manager.transition_to(Screen.START)
    
    def handle_text_input(self, event: pygame.event.Event,
                         ui_manager: 'UIManager') -> bool:
        """Handle text input for name entry.
        
        Processes keyboard events for entering player names:
        - Character keys: Add character to name
        - BACKSPACE: Remove last character
        - SPACE: Add space character
        - ENTER: Submit name (returns True)
        
        Args:
            event: Pygame keyboard event (must be KEYDOWN type)
            ui_manager: The UIManager instance containing name entry state
        
        Returns:
            True if ENTER was pressed (name submitted), False otherwise
        """
        if event.type != pygame.KEYDOWN:
            return False
        
        # Let UIManager handle the character input
        ui_manager.handle_name_entry_input(event)
        
        # Check if ENTER was pressed to submit
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            return True
        
        return False
    
    def handle_event(self, event: pygame.event.Event,
                    game_state: 'GameState',
                    ui_manager: 'UIManager') -> bool:
        """Handle a single Pygame event based on current screen state.
        
        This is a convenience method that routes events to the appropriate
        handler based on the current UI screen. It's the main entry point
        for event processing in the game loop.
        
        Args:
            event: Pygame event to process
            game_state: The GameState instance
            ui_manager: The UIManager instance
        
        Returns:
            True if the event was a name submission (ENTER in NAME_ENTRY screen),
            False otherwise
        """
        # Import Screen enum here to avoid circular imports
        from tetris.views.ui_screens import Screen
        
        if ui_manager.current_screen == Screen.GAME:
            # During gameplay, handle game input
            if not game_state.game_over:
                self.handle_game_input(event, game_state)
        
        elif ui_manager.current_screen == Screen.NAME_ENTRY:
            # During name entry, handle text input
            return self.handle_text_input(event, ui_manager)
        
        else:
            # In menu screens, handle menu input
            self.handle_menu_input(event, ui_manager, game_state)
        
        return False
