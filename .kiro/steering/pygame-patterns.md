---
inclusion: fileMatch
fileMatchPattern: '**/*.py'
---

# Pygame Patterns and Best Practices

## Overview

This document defines patterns and best practices for using Pygame in the Tetris clone project. These guidelines ensure efficient, maintainable, and bug-free Pygame code.

## Pygame Initialization

### Standard Initialization Sequence
```python
import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TETRIS")
    
    # Create clock for frame rate control
    clock = pygame.time.Clock()
    
    # Initialize font system
    pygame.font.init()
    
    # Game loop
    running = True
    while running:
        # ... game loop code ...
        clock.tick(60)  # 60 FPS
    
    # Cleanup
    pygame.quit()
    sys.exit()
```

### Initialization Best Practices
- Call `pygame.init()` once at startup
- Create display surface once and reuse
- Initialize font system explicitly if using text
- Always call `pygame.quit()` before exit

## Game Loop Structure

### Standard Game Loop Pattern
```python
def game_loop():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # 1. Calculate delta time
        delta_time = clock.tick(60) / 1000.0  # Convert to seconds
        
        # 2. Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # ... handle other events ...
        
        # 3. Update game state
        game_state.update(delta_time)
        
        # 4. Render
        renderer.render_game(game_state)
        pygame.display.flip()
    
    pygame.quit()
```

### Game Loop Principles
- **Fixed frame rate**: Use `clock.tick(60)` for consistent 60 FPS
- **Delta time**: Pass time delta to update for frame-independent movement
- **Event processing**: Handle all events every frame
- **Update before render**: Always update state before drawing
- **Single flip**: Call `pygame.display.flip()` once per frame

## Event Handling

### Event Processing Pattern
```python
def handle_events(game_state: GameState, ui_manager: UIManager):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Signal to exit
        
        elif event.type == pygame.KEYDOWN:
            if ui_manager.current_screen == Screen.GAME:
                handle_game_input(event, game_state)
            elif ui_manager.current_screen == Screen.NAME_ENTRY:
                handle_text_input(event, ui_manager)
            elif ui_manager.current_screen == Screen.START:
                handle_menu_input(event, ui_manager)
        
    return True  # Continue running
```

### Event Handling Best Practices
- Process all events every frame (don't skip)
- Use `pygame.QUIT` to handle window close
- Use `pygame.KEYDOWN` for discrete actions (move, rotate)
- Don't use `pygame.KEYUP` unless you need it
- Route events based on current game state/screen

### Keyboard Input Mapping
```python
def handle_game_input(event: pygame.event.Event, game_state: GameState):
    if event.key == pygame.K_LEFT:
        game_state.move_active_left()
    elif event.key == pygame.K_RIGHT:
        game_state.move_active_right()
    elif event.key == pygame.K_SPACE:
        game_state.rotate_active()
    elif event.key == pygame.K_DOWN:
        game_state.hard_drop()
    elif event.key == pygame.K_ESCAPE:
        # Pause or quit
        pass
```

## Rendering Patterns

### Rendering Order
Always render in this order:
1. Clear screen (fill with background color)
2. Draw background elements (grid lines, borders)
3. Draw game elements (stopped blocks, active tetromino)
4. Draw UI elements (score, text)
5. Flip display

### Example Rendering Method
```python
def render_game(self, game_state: GameState):
    # 1. Clear screen
    self.screen.fill(self.BACKGROUND_COLOR)
    
    # 2. Draw grid
    self.draw_grid_lines()
    
    # 3. Draw playfield (stopped blocks)
    self.draw_playfield(game_state.playfield)
    
    # 4. Draw active tetromino
    if game_state.active_tetromino:
        self.draw_tetromino(game_state.active_tetromino)
    
    # 5. Draw score
    self.draw_score(game_state.score)
    
    # 6. Flip display (done in main loop)
```

### Rendering Best Practices
- Clear screen every frame (don't rely on overdraw)
- Draw from back to front (background → foreground)
- Minimize draw calls (batch similar operations)
- Use `pygame.display.flip()` not `pygame.display.update()` (simpler)

## Drawing Primitives

### Drawing Rectangles (Blocks)
```python
def draw_block(self, x: int, y: int, color: Tuple[int, int, int]):
    """Draw a single block at grid position (x, y)."""
    screen_x = self.offset_x + x * self.block_size
    screen_y = self.offset_y + y * self.block_size
    
    rect = pygame.Rect(screen_x, screen_y, self.block_size, self.block_size)
    pygame.draw.rect(self.screen, color, rect)
    
    # Optional: Draw border for visual separation
    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
```

### Drawing Lines (Grid)
```python
def draw_grid_lines(self):
    """Draw playfield border and grid lines."""
    # Outer border
    border_rect = pygame.Rect(
        self.offset_x - 2,
        self.offset_y - 2,
        PLAYFIELD_WIDTH * self.block_size + 4,
        PLAYFIELD_HEIGHT * self.block_size + 4
    )
    pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2)
    
    # Optional: Internal grid lines
    for x in range(PLAYFIELD_WIDTH + 1):
        start_pos = (self.offset_x + x * self.block_size, self.offset_y)
        end_pos = (self.offset_x + x * self.block_size, 
                   self.offset_y + PLAYFIELD_HEIGHT * self.block_size)
        pygame.draw.line(self.screen, (50, 50, 50), start_pos, end_pos, 1)
```

### Drawing Best Practices
- Use `pygame.Rect` for rectangle operations
- Cache frequently used rectangles
- Use integer coordinates (Pygame uses pixels)
- Draw borders after fills for clean edges

## Text Rendering

### Font Management
```python
class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        # Load fonts once
        self.title_font = pygame.font.Font(None, 72)  # Large for title
        self.score_font = pygame.font.Font(None, 36)  # Medium for score
        self.text_font = pygame.font.Font(None, 24)   # Small for text
```

### Rendering Text
```python
def draw_text(self, text: str, font: pygame.font.Font, 
              color: Tuple[int, int, int], x: int, y: int, 
              center: bool = False):
    """Draw text at specified position."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    self.screen.blit(text_surface, text_rect)
```

### Text Rendering Best Practices
- Load fonts once, reuse them
- Use `None` for default Pygame font (always available)
- Use `True` for antialiasing (smoother text)
- Cache rendered text surfaces if text doesn't change
- Center important text (titles, game over messages)

## Color Management

### Define Colors as Constants
```python
# Color constants (RGB tuples)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)

# Tetromino colors
CYAN = (0, 255, 255)      # I-piece
YELLOW = (255, 255, 0)    # O-piece
PURPLE = (128, 0, 128)    # T-piece
ORANGE = (255, 165, 0)    # L-piece
BLUE = (0, 0, 255)        # J-piece
GREEN = (0, 255, 0)       # S-piece
RED = (255, 0, 0)         # Z-piece

# UI colors
BACKGROUND_COLOR = (20, 20, 20)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
```

### Color Best Practices
- Define colors as module-level constants
- Use descriptive names (not `COLOR1`, `COLOR2`)
- Use RGB tuples (0-255 for each channel)
- Consider color-blind friendly palettes
- Keep colors consistent across the game

## Coordinate Systems

### Grid to Screen Conversion
```python
def grid_to_screen(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
    """Convert grid coordinates to screen pixel coordinates."""
    screen_x = self.offset_x + grid_x * self.block_size
    screen_y = self.offset_y + grid_y * self.block_size
    return screen_x, screen_y

def screen_to_grid(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
    """Convert screen pixel coordinates to grid coordinates."""
    grid_x = (screen_x - self.offset_x) // self.block_size
    grid_y = (screen_y - self.offset_y) // self.block_size
    return grid_x, grid_y
```

### Coordinate System Best Practices
- Keep grid coordinates separate from screen coordinates
- Use conversion functions consistently
- Grid coordinates: (0, 0) is top-left of playfield
- Screen coordinates: (0, 0) is top-left of window
- Document which coordinate system each function uses

## Performance Optimization

### Efficient Rendering
```python
# Good - Only redraw what changed
def render_game(self, game_state: GameState):
    if game_state.needs_redraw:
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_everything(game_state)
        game_state.needs_redraw = False

# For this project: Don't optimize prematurely
# Redraw everything every frame - it's fast enough
def render_game(self, game_state: GameState):
    self.screen.fill(self.BACKGROUND_COLOR)
    self.draw_everything(game_state)
```

### Performance Best Practices
- For Tetris: Full redraw every frame is fine (simple game)
- Avoid creating new surfaces every frame
- Reuse font objects
- Don't optimize until you measure a problem
- 60 FPS is easy to achieve for this game

## Screen Management

### Multiple Screens Pattern
```python
class UIManager:
    def render(self, screen: pygame.Surface, game_state: GameState):
        if self.current_screen == Screen.START:
            self.render_start_screen(screen)
        elif self.current_screen == Screen.GAME:
            self.render_game_screen(screen, game_state)
        elif self.current_screen == Screen.GAME_OVER:
            self.render_game_over_screen(screen, game_state.score)
        elif self.current_screen == Screen.NAME_ENTRY:
            self.render_name_entry_screen(screen, game_state.score)
        elif self.current_screen == Screen.HIGH_SCORES:
            self.render_high_scores_screen(screen)
```

### Screen Management Best Practices
- Use enum for screen states
- Single render method that dispatches to screen-specific methods
- Clear screen at start of each screen render
- Handle transitions in a centralized place

## Common Pygame Pitfalls

### ❌ Forgetting to Process Events
```python
# Bad - Events queue up and game becomes unresponsive
while running:
    game_state.update(0.016)
    render()
```

### ✅ Always Process Events
```python
# Good
while running:
    for event in pygame.event.get():
        handle_event(event)
    game_state.update(0.016)
    render()
```

### ❌ Not Using Delta Time
```python
# Bad - Movement speed depends on frame rate
def update(self):
    self.y += 1  # Moves faster on faster computers
```

### ✅ Use Delta Time
```python
# Good - Movement speed is consistent
def update(self, delta_time: float):
    self.y += self.speed * delta_time  # Frame-independent
```

### ❌ Creating Fonts Every Frame
```python
# Bad - Very slow
def render_score(self, score: int):
    font = pygame.font.Font(None, 36)  # Created every frame!
    text = font.render(f"Score: {score}", True, WHITE)
```

### ✅ Reuse Fonts
```python
# Good - Font created once
def __init__(self):
    self.score_font = pygame.font.Font(None, 36)

def render_score(self, score: int):
    text = self.score_font.render(f"Score: {score}", True, WHITE)
```

## Testing Pygame Code

### Mocking Pygame for Tests
```python
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def mock_screen():
    screen = MagicMock(spec=pygame.Surface)
    return screen

def test_renderer_draws_block(mock_screen):
    renderer = Renderer(screen=mock_screen)
    renderer.draw_block(5, 10, (255, 0, 0))
    
    # Verify pygame.draw.rect was called
    assert mock_screen.blit.called or pygame.draw.rect.called
```

### Testing Best Practices
- Mock Pygame surfaces for unit tests
- Test rendering logic without actual display
- Integration tests can use real Pygame (headless mode)
- Focus tests on logic, not pixel-perfect rendering

## Pygame Resources

### Official Documentation
- Pygame docs: https://www.pygame.org/docs/
- Pygame tutorials: https://www.pygame.org/wiki/tutorials

### Common Pygame Modules Used
- `pygame.display`: Window and screen management
- `pygame.draw`: Drawing primitives (rect, line, circle)
- `pygame.font`: Text rendering
- `pygame.event`: Event handling
- `pygame.time`: Timing and frame rate control
- `pygame.key`: Keyboard state

### Pygame Constants Used
- `pygame.QUIT`: Window close event
- `pygame.KEYDOWN`: Key press event
- `pygame.K_LEFT`, `pygame.K_RIGHT`, etc.: Key codes
- `pygame.K_SPACE`, `pygame.K_ESCAPE`: Special keys

## Pygame Checklist

Before considering Pygame code complete:
- [ ] `pygame.init()` called once at startup
- [ ] Events processed every frame
- [ ] Frame rate controlled with `clock.tick(60)`
- [ ] Delta time used for frame-independent movement
- [ ] Fonts loaded once and reused
- [ ] Colors defined as constants
- [ ] Screen cleared every frame
- [ ] `pygame.display.flip()` called once per frame
- [ ] `pygame.quit()` called before exit
- [ ] Coordinate conversion functions used consistently
