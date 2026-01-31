"""Integration tests for Tetris game loop.

This module tests the integration of all components working together:
- Complete game flow from start to game over
- High score qualification and name entry flow
- Game state immutability after game over
- Component coordination and transitions

These tests verify that the model, view, and controller layers work
together correctly to create a complete game experience.
"""

import tempfile
import os
from unittest.mock import MagicMock, Mock, patch

import pytest
import pygame

from tetris.controllers.input_handler import InputHandler
from tetris.models.game_state import GameState
from tetris.models.high_scores import HighScoreManager
from tetris.views.renderer import Renderer
from tetris.views.ui_screens import UIManager, Screen


@pytest.fixture
def mock_screen():
    """Provide a mock Pygame surface for testing."""
    screen = MagicMock(spec=pygame.Surface)
    screen.fill = Mock()
    screen.blit = Mock()
    return screen


@pytest.fixture
def temp_high_score_file():
    """Provide a temporary file for high score testing."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def game_components(mock_screen, temp_high_score_file):
    """Provide all game components initialized and ready to use."""
    # Initialize Pygame (required for font system)
    pygame.init()
    pygame.font.init()
    
    game_state = GameState()
    renderer = Renderer(mock_screen)
    ui_manager = UIManager(mock_screen)
    input_handler = InputHandler()
    high_score_manager = HighScoreManager(file_path=temp_high_score_file)
    
    yield {
        'game_state': game_state,
        'renderer': renderer,
        'ui_manager': ui_manager,
        'input_handler': input_handler,
        'high_score_manager': high_score_manager,
        'screen': mock_screen
    }
    
    # Cleanup Pygame
    pygame.quit()


class TestCompleteGameFlow:
    """Test complete game flow from start to game over.
    
    Validates: Requirements 7.1, 7.2, 7.3
    """
    
    def test_start_to_game_transition(self, game_components):
        """Test transition from start screen to game screen."""
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        input_handler = game_components['input_handler']
        
        # Start at START screen
        assert ui_manager.current_screen == Screen.START
        assert game_state.active_tetromino is None
        
        # Simulate SPACE key press to start game
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        
        input_handler.handle_menu_input(event, ui_manager, game_state)
        
        # Should transition to GAME screen and spawn tetromino
        assert ui_manager.current_screen == Screen.GAME
        assert game_state.active_tetromino is not None
        assert game_state.score == 0
        assert not game_state.game_over
    
    def test_game_to_game_over_transition(self, game_components):
        """Test transition from game to game over screen."""
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        high_score_manager = game_components['high_score_manager']
        
        # Start game
        ui_manager.transition_to(Screen.GAME)
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Force game over by filling top row
        for x in range(10):
            game_state.playfield.set_cell(x, 0, (255, 0, 0))
        
        # Lock a tetromino to trigger game over check
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Check game over transition logic
        assert game_state.game_over
        
        # If score doesn't qualify, should go to GAME_OVER screen
        if not high_score_manager.is_high_score(game_state.score):
            ui_manager.transition_to(Screen.GAME_OVER)
            assert ui_manager.current_screen == Screen.GAME_OVER
    
    def test_complete_game_cycle(self, game_components):
        """Test a complete game cycle: start → game → game over → restart."""
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        input_handler = game_components['input_handler']
        
        # 1. Start screen
        assert ui_manager.current_screen == Screen.START
        
        # 2. Start game
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        input_handler.handle_menu_input(event, ui_manager, game_state)
        assert ui_manager.current_screen == Screen.GAME
        
        # 3. Play game (simulate some moves)
        initial_tetromino = game_state.active_tetromino
        assert initial_tetromino is not None
        
        # Move left
        game_state.move_active_left()
        assert game_state.active_tetromino.x == initial_tetromino.x - 1
        
        # Move right
        game_state.move_active_right()
        assert game_state.active_tetromino.x == initial_tetromino.x
        
        # 4. Force game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # 5. Transition to game over screen
        ui_manager.transition_to(Screen.GAME_OVER)
        assert ui_manager.current_screen == Screen.GAME_OVER
        
        # 6. Return to start screen
        input_handler.handle_menu_input(event, ui_manager, game_state)
        # Note: From GAME_OVER, SPACE doesn't automatically go to START
        # It would need to go through high scores first
        ui_manager.transition_to(Screen.HIGH_SCORES)
        assert ui_manager.current_screen == Screen.HIGH_SCORES
        
        # 7. Return to start
        input_handler.handle_menu_input(event, ui_manager, game_state)
        assert ui_manager.current_screen == Screen.START
    
    def test_game_update_loop(self, game_components):
        """Test game state updates during gameplay."""
        game_state = game_components['game_state']
        ui_manager = game_components['ui_manager']
        
        # Start game
        ui_manager.transition_to(Screen.GAME)
        game_state.reset()
        game_state.spawn_tetromino()
        
        initial_y = game_state.active_tetromino.y
        
        # Simulate multiple update cycles
        for _ in range(10):
            game_state.update(0.1)  # 100ms per update
        
        # After 1 second (10 * 0.1s), tetromino should have fallen
        # (default fall interval is 0.5s, so it should fall twice)
        assert game_state.active_tetromino.y >= initial_y + 2
    
    def test_rendering_all_screens(self, game_components):
        """Test that all screens can be rendered without errors."""
        renderer = game_components['renderer']
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        high_score_manager = game_components['high_score_manager']
        screen = game_components['screen']
        
        # Mock pygame.draw methods in both renderer and ui_screens modules
        with patch('tetris.views.renderer.pygame.draw.rect'), \
             patch('tetris.views.renderer.pygame.draw.line'), \
             patch('tetris.views.ui_screens.pygame.draw.rect'), \
             patch('tetris.views.ui_screens.pygame.draw.line'):
            
            # Start screen
            ui_manager.transition_to(Screen.START)
            ui_manager.render_start_screen()
            assert screen.fill.called
            
            # Game screen
            ui_manager.transition_to(Screen.GAME)
            game_state.reset()
            game_state.spawn_tetromino()
            renderer.render_game(game_state)
            assert screen.fill.called
            
            # Game over screen
            ui_manager.transition_to(Screen.GAME_OVER)
            ui_manager.render_game_over_screen(1000)
            assert screen.fill.called
            
            # Name entry screen
            ui_manager.transition_to(Screen.NAME_ENTRY)
            ui_manager.render_name_entry_screen(1000)
            assert screen.fill.called
            
            # High scores screen
            ui_manager.transition_to(Screen.HIGH_SCORES)
            ui_manager.render_high_scores_screen(high_score_manager.get_top_scores())
            assert screen.fill.called


class TestHighScoreFlow:
    """Test high score qualification and name entry flow.
    
    Validates: Requirements 8.4, 8.5, 9.1
    """
    
    def test_high_score_qualification_flow(self, game_components):
        """Test flow when score qualifies for high score list."""
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        high_score_manager = game_components['high_score_manager']
        
        # Start game and achieve a high score
        ui_manager.transition_to(Screen.GAME)
        game_state.reset()
        game_state.spawn_tetromino()
        game_state.score = 1000  # Set a high score
        
        # Trigger game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Check if score qualifies
        assert high_score_manager.is_high_score(game_state.score)
        
        # Should transition to NAME_ENTRY screen
        ui_manager.transition_to(Screen.NAME_ENTRY)
        assert ui_manager.current_screen == Screen.NAME_ENTRY
        assert ui_manager.player_name == ""  # Name should be reset
    
    def test_name_entry_and_submission(self, game_components):
        """Test entering name and submitting high score."""
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        high_score_manager = game_components['high_score_manager']
        input_handler = game_components['input_handler']
        
        # Set up high score scenario
        game_state.score = 1000
        ui_manager.transition_to(Screen.NAME_ENTRY)
        
        # Simulate typing "ALICE"
        for char in "ALICE":
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = ord(char)
            event.unicode = char
            ui_manager.handle_name_entry_input(event)
        
        assert ui_manager.player_name == "ALICE"
        
        # Submit with ENTER
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RETURN
        event.unicode = '\r'
        
        submitted = input_handler.handle_text_input(event, ui_manager)
        assert submitted
        
        # Add score to high score manager
        high_score_manager.add_score(ui_manager.player_name.strip(), game_state.score)
        
        # Verify score was added
        top_scores = high_score_manager.get_top_scores()
        assert len(top_scores) == 1
        assert top_scores[0].name == "ALICE"
        assert top_scores[0].score == 1000
    
    def test_non_qualifying_score_flow(self, game_components):
        """Test flow when score doesn't qualify for high score list."""
        ui_manager = game_components['ui_manager']
        game_state = game_components['game_state']
        high_score_manager = game_components['high_score_manager']
        
        # Fill high score list with better scores
        for i in range(10):
            high_score_manager.add_score(f"Player{i}", 1000 + i * 100)
        
        # Start game with low score
        ui_manager.transition_to(Screen.GAME)
        game_state.reset()
        game_state.spawn_tetromino()
        game_state.score = 100  # Low score
        
        # Trigger game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Check if score qualifies (should not)
        assert not high_score_manager.is_high_score(game_state.score)
        
        # Should transition directly to GAME_OVER screen (not NAME_ENTRY)
        ui_manager.transition_to(Screen.GAME_OVER)
        assert ui_manager.current_screen == Screen.GAME_OVER
    
    def test_high_score_persistence(self, game_components):
        """Test that high scores persist across sessions."""
        high_score_manager = game_components['high_score_manager']
        temp_file = high_score_manager.file_path
        
        # Add some scores
        high_score_manager.add_score("ALICE", 1000)
        high_score_manager.add_score("BOB", 800)
        high_score_manager.save()
        
        # Create new manager with same file
        new_manager = HighScoreManager(file_path=temp_file)
        
        # Verify scores were loaded
        scores = new_manager.get_top_scores()
        assert len(scores) == 2
        assert scores[0].name == "ALICE"
        assert scores[0].score == 1000
        assert scores[1].name == "BOB"
        assert scores[1].score == 800
    
    def test_name_entry_backspace(self, game_components):
        """Test backspace functionality in name entry."""
        ui_manager = game_components['ui_manager']
        
        ui_manager.transition_to(Screen.NAME_ENTRY)
        
        # Type some characters
        for char in "TEST":
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = ord(char)
            event.unicode = char
            ui_manager.handle_name_entry_input(event)
        
        assert ui_manager.player_name == "TEST"
        
        # Press backspace twice
        for _ in range(2):
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = pygame.K_BACKSPACE
            event.unicode = '\b'
            ui_manager.handle_name_entry_input(event)
        
        assert ui_manager.player_name == "TE"


class TestGameStateImmutability:
    """Test that game state doesn't change after game over.
    
    Validates: Requirements 7.3
    """
    
    def test_no_movement_after_game_over(self, game_components):
        """Test that tetromino cannot move after game over."""
        game_state = game_components['game_state']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Trigger game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Try to move (should have no effect)
        result = game_state.move_active_left()
        assert not result
        assert game_state.active_tetromino is None
        
        result = game_state.move_active_right()
        assert not result
        assert game_state.active_tetromino is None
    
    def test_no_rotation_after_game_over(self, game_components):
        """Test that tetromino cannot rotate after game over."""
        game_state = game_components['game_state']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Trigger game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Try to rotate (should have no effect)
        result = game_state.rotate_active()
        assert not result
        assert game_state.active_tetromino is None
    
    def test_no_hard_drop_after_game_over(self, game_components):
        """Test that hard drop has no effect after game over."""
        game_state = game_components['game_state']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Trigger game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Try to hard drop (should have no effect)
        game_state.hard_drop()
        assert game_state.active_tetromino is None
    
    def test_no_update_after_game_over(self, game_components):
        """Test that game state doesn't update after game over."""
        game_state = game_components['game_state']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Trigger game over
        game_state.game_over = True
        final_score = game_state.score
        game_state.active_tetromino = None
        
        # Try to update (should have no effect)
        game_state.update(1.0)  # 1 second
        
        assert game_state.game_over
        assert game_state.active_tetromino is None
        assert game_state.score == final_score
    
    def test_no_spawn_after_game_over(self, game_components):
        """Test that new tetromino cannot spawn after game over."""
        game_state = game_components['game_state']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Trigger game over
        game_state.game_over = True
        game_state.active_tetromino = None
        
        # Try to spawn (should return None)
        result = game_state.spawn_tetromino()
        assert result is None
        assert game_state.active_tetromino is None
    
    def test_game_state_frozen_after_game_over(self, game_components):
        """Test that entire game state is frozen after game over."""
        game_state = game_components['game_state']
        
        # Start game and play a bit
        game_state.reset()
        game_state.spawn_tetromino()
        game_state.score = 100
        
        # Capture state before game over
        playfield_state = [[game_state.playfield.get_cell(x, y) 
                           for y in range(20)] for x in range(10)]
        
        # Trigger game over
        game_state.game_over = True
        final_score = game_state.score
        game_state.active_tetromino = None
        
        # Try various operations
        game_state.move_active_left()
        game_state.move_active_right()
        game_state.rotate_active()
        game_state.hard_drop()
        game_state.update(1.0)
        game_state.spawn_tetromino()
        
        # Verify nothing changed
        assert game_state.game_over
        assert game_state.score == final_score
        assert game_state.active_tetromino is None
        
        # Verify playfield unchanged
        for x in range(10):
            for y in range(20):
                assert game_state.playfield.get_cell(x, y) == playfield_state[x][y]


class TestComponentIntegration:
    """Test integration between different components."""
    
    def test_input_handler_game_state_integration(self, game_components):
        """Test input handler correctly controls game state."""
        game_state = game_components['game_state']
        input_handler = game_components['input_handler']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        initial_x = game_state.active_tetromino.x
        initial_rotation = game_state.active_tetromino.rotation
        
        # Simulate left arrow key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_LEFT
        input_handler.handle_game_input(event, game_state)
        assert game_state.active_tetromino.x == initial_x - 1
        
        # Simulate right arrow key
        event.key = pygame.K_RIGHT
        input_handler.handle_game_input(event, game_state)
        assert game_state.active_tetromino.x == initial_x
        
        # Simulate space (rotate)
        event.key = pygame.K_SPACE
        input_handler.handle_game_input(event, game_state)
        assert game_state.active_tetromino.rotation != initial_rotation
    
    def test_ui_manager_screen_transitions(self, game_components):
        """Test UI manager handles screen transitions correctly."""
        ui_manager = game_components['ui_manager']
        
        # Test all transitions
        ui_manager.transition_to(Screen.START)
        assert ui_manager.current_screen == Screen.START
        
        ui_manager.transition_to(Screen.GAME)
        assert ui_manager.current_screen == Screen.GAME
        
        ui_manager.transition_to(Screen.GAME_OVER)
        assert ui_manager.current_screen == Screen.GAME_OVER
        
        ui_manager.transition_to(Screen.NAME_ENTRY)
        assert ui_manager.current_screen == Screen.NAME_ENTRY
        assert ui_manager.player_name == ""  # Should reset
        
        ui_manager.transition_to(Screen.HIGH_SCORES)
        assert ui_manager.current_screen == Screen.HIGH_SCORES
    
    def test_renderer_game_state_integration(self, game_components):
        """Test renderer correctly reads from game state."""
        renderer = game_components['renderer']
        game_state = game_components['game_state']
        screen = game_components['screen']
        
        # Start game
        game_state.reset()
        game_state.spawn_tetromino()
        
        # Mock pygame.draw methods in renderer module to avoid Surface type checking
        with patch('tetris.views.renderer.pygame.draw.rect'), \
             patch('tetris.views.renderer.pygame.draw.line'):
            
            # Render game
            renderer.render_game(game_state)
            
            # Verify rendering methods were called
            assert screen.fill.called
            # Note: We can't easily verify specific draw calls without
            # more detailed mocking, but we can verify no exceptions occurred
    
    def test_high_score_manager_integration(self, game_components):
        """Test high score manager integrates with game flow."""
        game_state = game_components['game_state']
        high_score_manager = game_components['high_score_manager']
        
        # Play game and get score
        game_state.reset()
        game_state.spawn_tetromino()
        game_state.score = 500
        
        # Check if qualifies
        qualifies = high_score_manager.is_high_score(game_state.score)
        assert qualifies  # Should qualify for empty list
        
        # Add score
        high_score_manager.add_score("TEST", game_state.score)
        
        # Verify it's in the list
        scores = high_score_manager.get_top_scores()
        assert len(scores) == 1
        assert scores[0].score == 500
        assert scores[0].name == "TEST"
