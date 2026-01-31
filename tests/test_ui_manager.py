"""Unit tests for UIManager class.

Tests UI screen transitions and rendering methods.
"""

from unittest.mock import MagicMock, Mock
import pytest
import pygame

from tetris.views.ui_screens import UIManager, Screen
from tetris.models.high_scores import HighScoreEntry


@pytest.fixture
def mock_screen():
    """Provide a mock Pygame surface for testing."""
    screen = MagicMock()
    screen.fill = Mock()
    screen.blit = Mock()
    return screen


@pytest.fixture
def ui_manager(mock_screen):
    """Provide a UIManager instance with mock screen."""
    # Ensure pygame is initialized (may have been quit by other tests)
    if not pygame.get_init():
        pygame.init()
    pygame.font.init()
    return UIManager(screen=mock_screen)


def test_ui_manager_initializes_with_start_screen(ui_manager):
    """Test that UIManager initializes with START screen."""
    assert ui_manager.current_screen == Screen.START


def test_transition_to_game_screen(ui_manager):
    """Test START → GAME transition."""
    ui_manager.transition_to(Screen.GAME)
    assert ui_manager.current_screen == Screen.GAME


def test_transition_to_game_over_screen(ui_manager):
    """Test GAME → GAME_OVER transition."""
    ui_manager.transition_to(Screen.GAME)
    ui_manager.transition_to(Screen.GAME_OVER)
    assert ui_manager.current_screen == Screen.GAME_OVER


def test_transition_to_name_entry_screen(ui_manager):
    """Test GAME_OVER → NAME_ENTRY transition (when high score achieved)."""
    ui_manager.transition_to(Screen.GAME_OVER)
    ui_manager.transition_to(Screen.NAME_ENTRY)
    assert ui_manager.current_screen == Screen.NAME_ENTRY


def test_transition_to_name_entry_resets_player_name(ui_manager):
    """Test that transitioning to NAME_ENTRY resets player name."""
    ui_manager.player_name = "OLD_NAME"
    ui_manager.transition_to(Screen.NAME_ENTRY)
    assert ui_manager.player_name == ""


def test_transition_to_high_scores_screen(ui_manager):
    """Test NAME_ENTRY → HIGH_SCORES transition."""
    ui_manager.transition_to(Screen.NAME_ENTRY)
    ui_manager.transition_to(Screen.HIGH_SCORES)
    assert ui_manager.current_screen == Screen.HIGH_SCORES


def test_render_start_screen_does_not_crash(ui_manager, mock_screen):
    """Test that rendering start screen doesn't crash."""
    ui_manager.render_start_screen()
    # Verify screen was filled (cleared)
    assert mock_screen.fill.called


def test_render_game_over_screen_does_not_crash(ui_manager, mock_screen):
    """Test that rendering game over screen doesn't crash."""
    ui_manager.render_game_over_screen(final_score=1000)
    # Verify screen was filled (cleared)
    assert mock_screen.fill.called


def test_render_name_entry_screen_does_not_crash(ui_manager, mock_screen):
    """Test that rendering name entry screen doesn't crash."""
    ui_manager.render_name_entry_screen(score=1500)
    # Verify screen was filled (cleared)
    assert mock_screen.fill.called


def test_render_high_scores_screen_with_empty_list(ui_manager, mock_screen):
    """Test that rendering high scores screen with empty list doesn't crash."""
    ui_manager.render_high_scores_screen(high_scores=[])
    # Verify screen was filled (cleared)
    assert mock_screen.fill.called


def test_render_high_scores_screen_with_scores(ui_manager, mock_screen):
    """Test that rendering high scores screen with scores doesn't crash."""
    scores = [
        HighScoreEntry(name="Alice", score=1000, timestamp="2024-01-01"),
        HighScoreEntry(name="Bob", score=900, timestamp="2024-01-02"),
        HighScoreEntry(name="Charlie", score=800, timestamp="2024-01-03"),
    ]
    ui_manager.render_high_scores_screen(high_scores=scores)
    # Verify screen was filled (cleared)
    assert mock_screen.fill.called


def test_handle_name_entry_input_adds_character(ui_manager):
    """Test that name entry adds characters correctly."""
    # Create a simple object that mimics pygame event
    # Use integer value directly to avoid mock issues
    from types import SimpleNamespace
    event = SimpleNamespace(type=768, key=97, unicode='A')  # 768 = KEYDOWN, 97 = K_a
    
    ui_manager.handle_name_entry_input(event)
    assert ui_manager.player_name == "A"


def test_handle_name_entry_input_adds_multiple_characters(ui_manager):
    """Test that name entry accumulates characters."""
    from types import SimpleNamespace
    
    # Use integer values directly to avoid mock issues
    events = [
        ('A', 97),   # K_a
        ('L', 108),  # K_l
        ('I', 105),  # K_i
        ('C', 99),   # K_c
        ('E', 101),  # K_e
    ]
    
    for char, key in events:
        event = SimpleNamespace(type=768, key=key, unicode=char)  # 768 = KEYDOWN
        ui_manager.handle_name_entry_input(event)
    
    assert ui_manager.player_name == "ALICE"


def test_handle_name_entry_input_backspace_removes_character(ui_manager):
    """Test that backspace removes last character."""
    ui_manager.player_name = "ALICE"
    
    from types import SimpleNamespace
    event = SimpleNamespace(type=768, key=8, unicode='\b')  # 768 = KEYDOWN, 8 = K_BACKSPACE
    
    ui_manager.handle_name_entry_input(event)
    assert ui_manager.player_name == "ALIC"


def test_handle_name_entry_input_backspace_on_empty_string(ui_manager):
    """Test that backspace on empty string doesn't crash."""
    ui_manager.player_name = ""
    
    from types import SimpleNamespace
    event = SimpleNamespace(type=768, key=8, unicode='\b')  # 768 = KEYDOWN, 8 = K_BACKSPACE
    
    ui_manager.handle_name_entry_input(event)
    assert ui_manager.player_name == ""


def test_handle_name_entry_input_space_adds_space(ui_manager):
    """Test that space key adds a space character."""
    ui_manager.player_name = "ALICE"
    
    from types import SimpleNamespace
    event = SimpleNamespace(type=768, key=32, unicode=' ')  # 768 = KEYDOWN, 32 = K_SPACE
    
    ui_manager.handle_name_entry_input(event)
    assert ui_manager.player_name == "ALICE "


def test_handle_name_entry_input_limits_name_length(ui_manager):
    """Test that name entry limits name to 20 characters."""
    ui_manager.player_name = "A" * 20
    
    from types import SimpleNamespace
    event = SimpleNamespace(type=768, key=98, unicode='B')  # 768 = KEYDOWN, 98 = K_b
    
    ui_manager.handle_name_entry_input(event)
    # Should still be 20 characters, not 21
    assert len(ui_manager.player_name) == 20
    assert ui_manager.player_name == "A" * 20


def test_handle_name_entry_input_ignores_non_printable_characters(ui_manager):
    """Test that non-printable characters are ignored."""
    ui_manager.player_name = "ALICE"
    
    from types import SimpleNamespace
    event = SimpleNamespace(type=768, key=9, unicode='\t')  # 768 = KEYDOWN, 9 = K_TAB
    
    ui_manager.handle_name_entry_input(event)
    # Name should be unchanged
    assert ui_manager.player_name == "ALICE"


def test_complete_screen_flow(ui_manager):
    """Test complete screen flow from start to high scores."""
    # Start at START screen
    assert ui_manager.current_screen == Screen.START
    
    # Transition to GAME
    ui_manager.transition_to(Screen.GAME)
    assert ui_manager.current_screen == Screen.GAME
    
    # Transition to GAME_OVER
    ui_manager.transition_to(Screen.GAME_OVER)
    assert ui_manager.current_screen == Screen.GAME_OVER
    
    # Transition to NAME_ENTRY (high score achieved)
    ui_manager.transition_to(Screen.NAME_ENTRY)
    assert ui_manager.current_screen == Screen.NAME_ENTRY
    assert ui_manager.player_name == ""  # Reset on transition
    
    # Transition to HIGH_SCORES
    ui_manager.transition_to(Screen.HIGH_SCORES)
    assert ui_manager.current_screen == Screen.HIGH_SCORES


def test_screen_flow_without_high_score(ui_manager):
    """Test screen flow when no high score is achieved."""
    # Start at START screen
    assert ui_manager.current_screen == Screen.START
    
    # Transition to GAME
    ui_manager.transition_to(Screen.GAME)
    assert ui_manager.current_screen == Screen.GAME
    
    # Transition to GAME_OVER
    ui_manager.transition_to(Screen.GAME_OVER)
    assert ui_manager.current_screen == Screen.GAME_OVER
    
    # Transition directly to HIGH_SCORES (skip NAME_ENTRY)
    ui_manager.transition_to(Screen.HIGH_SCORES)
    assert ui_manager.current_screen == Screen.HIGH_SCORES


def test_draw_text_helper_method(ui_manager, mock_screen):
    """Test that draw_text helper method works correctly."""
    # This is a basic smoke test - just verify it doesn't crash
    ui_manager.draw_text("Test", ui_manager.text_font, (255, 255, 255), 100, 100)
    assert mock_screen.blit.called


def test_draw_text_with_center_alignment(ui_manager, mock_screen):
    """Test that draw_text with center=True works correctly."""
    # This is a basic smoke test - just verify it doesn't crash
    ui_manager.draw_text("Test", ui_manager.text_font, (255, 255, 255), 400, 300, center=True)
    assert mock_screen.blit.called
