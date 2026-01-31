"""Unit tests for InputHandler class.

Tests input handling and routing to game state methods.
"""

from unittest.mock import MagicMock, Mock, call
import pytest
import pygame

from tetris.controllers.input_handler import InputHandler
from tetris.models.game_state import GameState
from tetris.views.ui_screens import UIManager, Screen


@pytest.fixture
def input_handler():
    """Provide an InputHandler instance."""
    return InputHandler()


@pytest.fixture
def mock_game_state():
    """Provide a mock GameState instance."""
    game_state = MagicMock(spec=GameState)
    game_state.game_over = False
    game_state.move_active_left = Mock(return_value=True)
    game_state.move_active_right = Mock(return_value=True)
    game_state.rotate_active = Mock(return_value=True)
    game_state.hard_drop = Mock()
    game_state.reset = Mock()
    game_state.spawn_tetromino = Mock()
    return game_state


@pytest.fixture
def mock_ui_manager():
    """Provide a mock UIManager instance."""
    # Initialize pygame for font system
    pygame.font.init()
    
    ui_manager = MagicMock(spec=UIManager)
    ui_manager.current_screen = Screen.START
    ui_manager.transition_to = Mock()
    ui_manager.handle_name_entry_input = Mock()
    ui_manager.player_name = ""
    return ui_manager


def create_keydown_event(key: int, unicode: str = "") -> pygame.event.Event:
    """Helper to create a KEYDOWN event."""
    event = MagicMock()
    event.type = pygame.KEYDOWN
    event.key = key
    event.unicode = unicode
    return event


def test_handle_game_input_left_arrow(input_handler, mock_game_state):
    """Test that LEFT ARROW calls move_active_left."""
    event = create_keydown_event(pygame.K_LEFT)
    
    input_handler.handle_game_input(event, mock_game_state)
    
    mock_game_state.move_active_left.assert_called_once()


def test_handle_game_input_right_arrow(input_handler, mock_game_state):
    """Test that RIGHT ARROW calls move_active_right."""
    event = create_keydown_event(pygame.K_RIGHT)
    
    input_handler.handle_game_input(event, mock_game_state)
    
    mock_game_state.move_active_right.assert_called_once()


def test_handle_game_input_space(input_handler, mock_game_state):
    """Test that SPACE calls rotate_active."""
    event = create_keydown_event(pygame.K_SPACE)
    
    input_handler.handle_game_input(event, mock_game_state)
    
    mock_game_state.rotate_active.assert_called_once()


def test_handle_game_input_down_arrow(input_handler, mock_game_state):
    """Test that DOWN ARROW calls hard_drop."""
    event = create_keydown_event(pygame.K_DOWN)
    
    input_handler.handle_game_input(event, mock_game_state)
    
    mock_game_state.hard_drop.assert_called_once()


def test_handle_game_input_ignores_non_keydown_events(input_handler, mock_game_state):
    """Test that non-KEYDOWN events are ignored."""
    event = MagicMock()
    event.type = pygame.KEYUP
    event.key = pygame.K_LEFT
    
    input_handler.handle_game_input(event, mock_game_state)
    
    # No methods should be called
    mock_game_state.move_active_left.assert_not_called()
    mock_game_state.move_active_right.assert_not_called()
    mock_game_state.rotate_active.assert_not_called()
    mock_game_state.hard_drop.assert_not_called()


def test_handle_game_input_ignores_other_keys(input_handler, mock_game_state):
    """Test that other keys are ignored during gameplay."""
    event = create_keydown_event(pygame.K_a)
    
    input_handler.handle_game_input(event, mock_game_state)
    
    # No methods should be called
    mock_game_state.move_active_left.assert_not_called()
    mock_game_state.move_active_right.assert_not_called()
    mock_game_state.rotate_active.assert_not_called()
    mock_game_state.hard_drop.assert_not_called()


def test_handle_menu_input_space_on_start_screen(input_handler, mock_ui_manager, mock_game_state):
    """Test that SPACE on START screen starts the game."""
    mock_ui_manager.current_screen = Screen.START
    event = create_keydown_event(pygame.K_SPACE)
    
    input_handler.handle_menu_input(event, mock_ui_manager, mock_game_state)
    
    # Should reset game state, spawn tetromino, and transition to GAME
    mock_game_state.reset.assert_called_once()
    mock_game_state.spawn_tetromino.assert_called_once()
    mock_ui_manager.transition_to.assert_called_once_with(Screen.GAME)


def test_handle_menu_input_space_on_high_scores_screen(input_handler, mock_ui_manager, mock_game_state):
    """Test that SPACE on HIGH_SCORES screen returns to START."""
    mock_ui_manager.current_screen = Screen.HIGH_SCORES
    event = create_keydown_event(pygame.K_SPACE)
    
    input_handler.handle_menu_input(event, mock_ui_manager, mock_game_state)
    
    # Should transition back to START
    mock_ui_manager.transition_to.assert_called_once_with(Screen.START)


def test_handle_menu_input_ignores_non_keydown_events(input_handler, mock_ui_manager, mock_game_state):
    """Test that non-KEYDOWN events are ignored in menus."""
    mock_ui_manager.current_screen = Screen.START
    event = MagicMock()
    event.type = pygame.KEYUP
    event.key = pygame.K_SPACE
    
    input_handler.handle_menu_input(event, mock_ui_manager, mock_game_state)
    
    # No transitions should occur
    mock_ui_manager.transition_to.assert_not_called()


def test_handle_text_input_delegates_to_ui_manager(input_handler, mock_ui_manager):
    """Test that text input is delegated to UIManager."""
    event = create_keydown_event(pygame.K_a, 'A')
    
    result = input_handler.handle_text_input(event, mock_ui_manager)
    
    # Should delegate to UIManager
    mock_ui_manager.handle_name_entry_input.assert_called_once_with(event)
    # Should return False (not ENTER)
    assert result is False


def test_handle_text_input_returns_true_on_enter(input_handler, mock_ui_manager):
    """Test that ENTER key returns True."""
    event = create_keydown_event(pygame.K_RETURN)
    
    result = input_handler.handle_text_input(event, mock_ui_manager)
    
    # Should return True to signal submission
    assert result is True


def test_handle_text_input_returns_true_on_keypad_enter(input_handler, mock_ui_manager):
    """Test that keypad ENTER also returns True."""
    event = create_keydown_event(pygame.K_KP_ENTER)
    
    result = input_handler.handle_text_input(event, mock_ui_manager)
    
    # Should return True to signal submission
    assert result is True


def test_handle_text_input_ignores_non_keydown_events(input_handler, mock_ui_manager):
    """Test that non-KEYDOWN events are ignored in text input."""
    event = MagicMock()
    event.type = pygame.KEYUP
    event.key = pygame.K_a
    
    result = input_handler.handle_text_input(event, mock_ui_manager)
    
    # Should not delegate to UIManager
    mock_ui_manager.handle_name_entry_input.assert_not_called()
    # Should return False
    assert result is False


def test_handle_event_routes_to_game_input_during_gameplay(input_handler, mock_game_state, mock_ui_manager):
    """Test that events are routed to game input during GAME screen."""
    mock_ui_manager.current_screen = Screen.GAME
    mock_game_state.game_over = False
    event = create_keydown_event(pygame.K_LEFT)
    
    input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Should call move_active_left
    mock_game_state.move_active_left.assert_called_once()


def test_handle_event_ignores_game_input_when_game_over(input_handler, mock_game_state, mock_ui_manager):
    """Test that game input is ignored when game is over."""
    mock_ui_manager.current_screen = Screen.GAME
    mock_game_state.game_over = True
    event = create_keydown_event(pygame.K_LEFT)
    
    input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Should not call move_active_left
    mock_game_state.move_active_left.assert_not_called()


def test_handle_event_routes_to_text_input_during_name_entry(input_handler, mock_game_state, mock_ui_manager):
    """Test that events are routed to text input during NAME_ENTRY screen."""
    mock_ui_manager.current_screen = Screen.NAME_ENTRY
    event = create_keydown_event(pygame.K_a, 'A')
    
    result = input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Should delegate to UIManager
    mock_ui_manager.handle_name_entry_input.assert_called_once_with(event)
    # Should return False (not ENTER)
    assert result is False


def test_handle_event_returns_true_on_name_submission(input_handler, mock_game_state, mock_ui_manager):
    """Test that ENTER during name entry returns True."""
    mock_ui_manager.current_screen = Screen.NAME_ENTRY
    event = create_keydown_event(pygame.K_RETURN)
    
    result = input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Should return True to signal submission
    assert result is True


def test_handle_event_routes_to_menu_input_on_start_screen(input_handler, mock_game_state, mock_ui_manager):
    """Test that events are routed to menu input on START screen."""
    mock_ui_manager.current_screen = Screen.START
    event = create_keydown_event(pygame.K_SPACE)
    
    input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Should start the game
    mock_game_state.reset.assert_called_once()
    mock_game_state.spawn_tetromino.assert_called_once()
    mock_ui_manager.transition_to.assert_called_once_with(Screen.GAME)


def test_handle_event_routes_to_menu_input_on_game_over_screen(input_handler, mock_game_state, mock_ui_manager):
    """Test that events are routed to menu input on GAME_OVER screen."""
    mock_ui_manager.current_screen = Screen.GAME_OVER
    event = create_keydown_event(pygame.K_SPACE)
    
    result = input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Menu input handler is called (but doesn't do anything for GAME_OVER + SPACE)
    # This is expected - the main loop handles the transition logic
    assert result is False


def test_handle_event_routes_to_menu_input_on_high_scores_screen(input_handler, mock_game_state, mock_ui_manager):
    """Test that events are routed to menu input on HIGH_SCORES screen."""
    mock_ui_manager.current_screen = Screen.HIGH_SCORES
    event = create_keydown_event(pygame.K_SPACE)
    
    input_handler.handle_event(event, mock_game_state, mock_ui_manager)
    
    # Should return to START screen
    mock_ui_manager.transition_to.assert_called_once_with(Screen.START)
