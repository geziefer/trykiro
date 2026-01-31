"""Main entry point for the Tetris Clone game.

This module contains the main game loop that orchestrates timing, event processing,
state updates, and rendering. It coordinates between the model, view, and controller
layers to create a complete game experience.

Usage:
    python -m tetris.main
"""

import sys

import pygame

from tetris.controllers.input_handler import InputHandler
from tetris.models.game_state import GameState
from tetris.models.high_scores import HighScoreManager
from tetris.views.renderer import Renderer, SCREEN_WIDTH, SCREEN_HEIGHT
from tetris.views.ui_screens import UIManager, Screen


def main() -> int:
    """Initialize and run the Tetris game.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Initialize Pygame
    try:
        pygame.init()
        pygame.font.init()
    except pygame.error as e:
        print(f"Failed to initialize Pygame: {e}", file=sys.stderr)
        return 1
    
    # Create display
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TETRIS")
    except pygame.error as e:
        print(f"Failed to create display: {e}", file=sys.stderr)
        pygame.quit()
        return 1
    
    # Create clock for frame rate control
    clock = pygame.time.Clock()
    
    # Initialize game components
    game_state = GameState()
    renderer = Renderer(screen)
    ui_manager = UIManager(screen)
    input_handler = InputHandler()
    high_score_manager = HighScoreManager()
    
    # Game over overlay state
    game_over_overlay_timer = 0.0
    game_over_overlay_duration = 2.0  # Show overlay for 2 seconds
    showing_game_over_overlay = False
    
    # Main game loop
    running = True
    while running:
        # 1. Calculate delta time (convert milliseconds to seconds)
        delta_time = clock.tick(60) / 1000.0  # 60 FPS
        
        # 2. Handle game over overlay timer
        if showing_game_over_overlay:
            game_over_overlay_timer += delta_time
            if game_over_overlay_timer >= game_over_overlay_duration:
                # Overlay time is up - transition to next screen
                showing_game_over_overlay = False
                game_over_overlay_timer = 0.0
                
                if high_score_manager.is_high_score(game_state.score):
                    ui_manager.transition_to(Screen.NAME_ENTRY)
                else:
                    ui_manager.transition_to(Screen.GAME_OVER)
        
        # 3. Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # Skip input during game over overlay
            if showing_game_over_overlay:
                continue
            
            # Route events based on current screen
            if ui_manager.current_screen == Screen.GAME:
                # During gameplay, handle game input
                if not game_state.game_over:
                    input_handler.handle_game_input(event, game_state)
            
            elif ui_manager.current_screen == Screen.NAME_ENTRY:
                # During name entry, handle text input
                if input_handler.handle_text_input(event, ui_manager):
                    # ENTER was pressed - submit the name
                    if ui_manager.player_name.strip():  # Only if name is not empty
                        high_score_manager.add_score(
                            ui_manager.player_name.strip(),
                            game_state.score
                        )
                        high_score_manager.save()
                    # Go back to start screen (which shows high scores)
                    ui_manager.transition_to(Screen.START)
            
            else:
                # In menu screens, handle menu input
                input_handler.handle_menu_input(event, ui_manager, game_state)
        
        # 4. Update game state (only during active gameplay)
        if ui_manager.current_screen == Screen.GAME and not game_state.game_over:
            game_state.update(delta_time)
        
        # 5. Check for game over transition
        if ui_manager.current_screen == Screen.GAME and game_state.game_over and not showing_game_over_overlay:
            # Game just ended - start showing overlay
            showing_game_over_overlay = True
            game_over_overlay_timer = 0.0
        
        # 6. Render current screen
        if ui_manager.current_screen == Screen.START:
            ui_manager.render_start_screen(high_score_manager.get_top_scores())
        
        elif ui_manager.current_screen == Screen.GAME:
            renderer.render_game(game_state)
            # Show game over overlay if active
            if showing_game_over_overlay:
                ui_manager.render_game_over_overlay(game_state.score)
        
        elif ui_manager.current_screen == Screen.GAME_OVER:
            ui_manager.render_game_over_screen(game_state.score)
        
        elif ui_manager.current_screen == Screen.NAME_ENTRY:
            ui_manager.render_name_entry_screen(game_state.score)
        
        # Note: HIGH_SCORES screen is not used - start screen shows high scores instead
        
        # 7. Update display
        pygame.display.flip()
    
    # Cleanup
    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
