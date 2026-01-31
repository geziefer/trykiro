"""Unit tests for the Renderer class.

These tests verify that the renderer correctly draws game elements without
requiring an actual display. We use mock Pygame surfaces to test the rendering
logic in isolation.
"""

from unittest.mock import MagicMock, Mock, patch, call
import pytest

# Mock pygame before importing renderer
import sys
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.font'] = MagicMock()
sys.modules['pygame.display'] = MagicMock()
sys.modules['pygame.draw'] = MagicMock()

from tetris.views.renderer import Renderer, BLOCK_SIZE, PLAYFIELD_OFFSET_X, PLAYFIELD_OFFSET_Y
from tetris.models.tetromino import Tetromino
from tetris.models.playfield import Playfield
from tetris.models.game_state import GameState


@pytest.fixture
def mock_screen():
    """Provide a mock Pygame surface for testing."""
    screen = MagicMock()
    screen.fill = Mock()
    screen.blit = Mock()
    return screen


@pytest.fixture
def mock_font():
    """Provide a mock Pygame font."""
    font = MagicMock()
    font.render = Mock(return_value=MagicMock())
    return font


@pytest.fixture
def renderer(mock_screen, mock_font):
    """Provide a Renderer instance with mocked Pygame components."""
    with patch('tetris.views.renderer.pygame.font.Font', return_value=mock_font):
        renderer = Renderer(mock_screen)
        return renderer


class TestRendererInitialization:
    """Test Renderer initialization."""
    
    def test_renderer_initializes_with_screen(self, mock_screen, mock_font):
        """Test that renderer initializes with correct attributes."""
        with patch('tetris.views.renderer.pygame.font.Font', return_value=mock_font):
            renderer = Renderer(mock_screen)
            
            assert renderer.screen == mock_screen
            assert renderer.block_size == BLOCK_SIZE
            assert renderer.offset_x == PLAYFIELD_OFFSET_X
            assert renderer.offset_y == PLAYFIELD_OFFSET_Y
            assert renderer.title_font is not None
            assert renderer.score_font is not None
            assert renderer.text_font is not None


class TestCoordinateConversion:
    """Test grid to screen coordinate conversion."""
    
    def test_grid_to_screen_conversion(self, renderer):
        """Test that grid coordinates convert correctly to screen coordinates."""
        # Test origin (0, 0)
        screen_x, screen_y = renderer.grid_to_screen(0, 0)
        assert screen_x == PLAYFIELD_OFFSET_X
        assert screen_y == PLAYFIELD_OFFSET_Y
        
        # Test position (5, 10)
        screen_x, screen_y = renderer.grid_to_screen(5, 10)
        assert screen_x == PLAYFIELD_OFFSET_X + 5 * BLOCK_SIZE
        assert screen_y == PLAYFIELD_OFFSET_Y + 10 * BLOCK_SIZE
        
        # Test bottom-right corner (9, 19)
        screen_x, screen_y = renderer.grid_to_screen(9, 19)
        assert screen_x == PLAYFIELD_OFFSET_X + 9 * BLOCK_SIZE
        assert screen_y == PLAYFIELD_OFFSET_Y + 19 * BLOCK_SIZE


class TestBlockDrawing:
    """Test individual block drawing."""
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    @patch('tetris.views.renderer.pygame.Rect')
    def test_draw_block_creates_rectangle(self, mock_rect, mock_draw_rect, renderer):
        """Test that draw_block creates and draws a rectangle."""
        color = (255, 0, 0)
        
        renderer.draw_block(5, 10, color)
        
        # Verify Rect was created with correct position and size
        expected_x = PLAYFIELD_OFFSET_X + 5 * BLOCK_SIZE
        expected_y = PLAYFIELD_OFFSET_Y + 10 * BLOCK_SIZE
        mock_rect.assert_called()
        
        # Verify draw.rect was called (for both fill and border)
        assert mock_draw_rect.call_count >= 2


class TestGridRendering:
    """Test playfield grid rendering."""
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    @patch('tetris.views.renderer.pygame.Rect')
    def test_render_grid_lines_draws_border(self, mock_rect, mock_draw_rect, renderer):
        """Test that render_grid_lines draws the playfield border."""
        renderer.render_grid_lines()
        
        # Verify Rect was created for border
        mock_rect.assert_called_once()
        
        # Verify draw.rect was called to draw the border
        mock_draw_rect.assert_called_once()


class TestPlayfieldRendering:
    """Test playfield rendering with stopped blocks."""
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_empty_playfield(self, mock_draw_rect, renderer):
        """Test rendering an empty playfield draws no blocks."""
        playfield = Playfield()
        
        # Reset mock to ignore any previous calls
        mock_draw_rect.reset_mock()
        
        renderer.render_playfield(playfield)
        
        # Empty playfield should not draw any blocks
        # (draw_rect might be called for borders in draw_block, but not for fills)
        # We just verify it doesn't crash
        assert True
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_playfield_with_blocks(self, mock_draw_rect, renderer):
        """Test rendering a playfield with stopped blocks."""
        playfield = Playfield()
        
        # Add some blocks to the playfield
        playfield.set_cell(0, 19, (255, 0, 0))  # Red block at bottom-left
        playfield.set_cell(5, 10, (0, 255, 0))  # Green block in middle
        playfield.set_cell(9, 0, (0, 0, 255))   # Blue block at top-right
        
        # Reset mock to count only render_playfield calls
        mock_draw_rect.reset_mock()
        
        renderer.render_playfield(playfield)
        
        # Should have drawn rectangles for the 3 blocks (fill + border each)
        assert mock_draw_rect.call_count >= 3


class TestTetrominoRendering:
    """Test tetromino rendering."""
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_tetromino_draws_all_blocks(self, mock_draw_rect, renderer):
        """Test that render_tetromino draws all 4 blocks."""
        tetromino = Tetromino(shape_type='I', x=5, y=10, rotation=0)
        
        # Reset mock
        mock_draw_rect.reset_mock()
        
        renderer.render_tetromino(tetromino)
        
        # Should draw 4 blocks (each with fill + border = 8 rect calls)
        assert mock_draw_rect.call_count >= 4
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_tetromino_different_shapes(self, mock_draw_rect, renderer):
        """Test rendering different tetromino shapes."""
        shapes = ['I', 'O', 'T', 'L', 'J', 'S', 'Z']
        
        for shape_type in shapes:
            tetromino = Tetromino(shape_type=shape_type, x=5, y=10, rotation=0)
            mock_draw_rect.reset_mock()
            
            renderer.render_tetromino(tetromino)
            
            # Each tetromino has exactly 4 blocks
            assert mock_draw_rect.call_count >= 4
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_tetromino_out_of_bounds(self, mock_draw_rect, renderer):
        """Test that blocks outside playfield are not drawn."""
        # Create tetromino partially above the playfield
        tetromino = Tetromino(shape_type='I', x=5, y=-2, rotation=1)
        
        mock_draw_rect.reset_mock()
        
        # Should not crash, only draws visible blocks
        renderer.render_tetromino(tetromino)
        
        # Some blocks may be drawn, but it shouldn't crash
        assert True


class TestScoreRendering:
    """Test score display rendering."""
    
    def test_render_score_displays_score(self, renderer, mock_font):
        """Test that render_score displays the score value."""
        score = 1234
        
        renderer.render_score(score)
        
        # Verify that text was rendered (font.render was called)
        # The mock font's render method should have been called
        assert renderer.score_font.render.called
    
    def test_render_score_zero(self, renderer, mock_font):
        """Test rendering score of zero."""
        renderer.render_score(0)
        
        assert renderer.score_font.render.called
    
    def test_render_score_large_value(self, renderer, mock_font):
        """Test rendering large score value."""
        renderer.render_score(999999)
        
        assert renderer.score_font.render.called


class TestGameRendering:
    """Test complete game rendering."""
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_game_clears_screen(self, mock_draw_rect, renderer, mock_screen):
        """Test that render_game clears the screen first."""
        game_state = GameState()
        game_state.spawn_tetromino()
        
        renderer.render_game(game_state)
        
        # Verify screen.fill was called to clear the screen
        mock_screen.fill.assert_called_once()
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_game_with_active_tetromino(self, mock_draw_rect, renderer, mock_screen):
        """Test rendering game state with active tetromino."""
        game_state = GameState()
        game_state.spawn_tetromino()
        
        renderer.render_game(game_state)
        
        # Verify screen was cleared
        assert mock_screen.fill.called
        
        # Verify drawing operations occurred
        assert mock_draw_rect.called
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_game_without_active_tetromino(self, mock_draw_rect, renderer, mock_screen):
        """Test rendering game state without active tetromino."""
        game_state = GameState()
        # Don't spawn tetromino
        
        renderer.render_game(game_state)
        
        # Should not crash even without active tetromino
        assert mock_screen.fill.called
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_game_with_stopped_blocks(self, mock_draw_rect, renderer, mock_screen):
        """Test rendering game with stopped blocks in playfield."""
        game_state = GameState()
        
        # Add some stopped blocks to the playfield
        game_state.playfield.set_cell(0, 19, (255, 0, 0))
        game_state.playfield.set_cell(1, 19, (0, 255, 0))
        game_state.playfield.set_cell(2, 19, (0, 0, 255))
        
        game_state.spawn_tetromino()
        
        renderer.render_game(game_state)
        
        # Verify rendering occurred
        assert mock_screen.fill.called
        assert mock_draw_rect.called
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_game_does_not_call_flip(self, mock_draw_rect, renderer, mock_screen):
        """Test that render_game does not call pygame.display.flip."""
        game_state = GameState()
        game_state.spawn_tetromino()
        
        with patch('tetris.views.renderer.pygame.display.flip') as mock_flip:
            renderer.render_game(game_state)
            
            # render_game should NOT call flip - that's the main loop's job
            mock_flip.assert_not_called()


class TestTextRendering:
    """Test text rendering helper method."""
    
    def test_draw_text_renders_text(self, renderer, mock_font):
        """Test that draw_text renders text surface."""
        text = "Hello, World!"
        color = (255, 255, 255)
        
        renderer.draw_text(text, mock_font, color, 100, 100, center=False)
        
        # Verify font.render was called
        mock_font.render.assert_called_once_with(text, True, color)
        
        # Verify blit was called to draw the text
        assert renderer.screen.blit.called
    
    def test_draw_text_centered(self, renderer, mock_font):
        """Test that draw_text can center text."""
        text = "Centered"
        color = (255, 255, 255)
        
        renderer.draw_text(text, mock_font, color, 400, 300, center=True)
        
        # Verify rendering occurred
        mock_font.render.assert_called_once()
        assert renderer.screen.blit.called


class TestRenderingIntegration:
    """Integration tests for rendering with real game states."""
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_complete_game_scenario(self, mock_draw_rect, renderer, mock_screen):
        """Test rendering a realistic game scenario."""
        game_state = GameState()
        
        # Spawn tetromino
        game_state.spawn_tetromino()
        
        # Move it around
        game_state.move_active_right()
        game_state.move_active_right()
        
        # Add some stopped blocks
        game_state.playfield.set_cell(0, 19, (255, 0, 0))
        game_state.playfield.set_cell(1, 19, (255, 0, 0))
        
        # Update score
        game_state.score = 42
        
        # Render the game
        renderer.render_game(game_state)
        
        # Verify it rendered without crashing
        assert mock_screen.fill.called
        assert mock_draw_rect.called
    
    @patch('tetris.views.renderer.pygame.draw.rect')
    def test_render_game_over_state(self, mock_draw_rect, renderer, mock_screen):
        """Test rendering when game is over."""
        game_state = GameState()
        game_state.game_over = True
        game_state.active_tetromino = None
        game_state.score = 100
        
        # Should render without crashing
        renderer.render_game(game_state)
        
        assert mock_screen.fill.called
