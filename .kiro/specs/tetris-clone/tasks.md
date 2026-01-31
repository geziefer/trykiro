# Implementation Plan: Tetris Clone

## Overview

This implementation plan breaks down the Tetris clone development into incremental, testable steps. The approach follows a bottom-up strategy: building core data structures first, then game logic, then rendering and UI. Each major component includes property-based tests to verify correctness across all possible inputs.

## Tasks

- [ ] 1. Set up project structure and dependencies
  - Create directory structure (tetris/models, tetris/views, tetris/controllers, tests/)
  - Create __init__.py files for all packages
  - Set up requirements.txt with pygame and hypothesis dependencies
  - Create main.py entry point skeleton
  - _Requirements: 11.1, 12.1_

- [ ] 2. Implement Tetromino class with shape definitions
  - [ ] 2.1 Create Tetromino class with shape type, color, position, and rotation attributes
    - Define all seven tetromino types with their block configurations
    - Implement shape rotation matrices for all four rotation states
    - Store color mappings for each tetromino type
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_
  
  - [ ] 2.2 Write unit tests for specific tetromino shapes
    - Test I-piece has correct cyan color and 4-block horizontal/vertical configurations
    - Test O-piece has correct yellow color and 2×2 square configuration
    - Test T, L, J, S, Z pieces have correct colors and shapes
    - _Requirements: 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_
  
  - [ ] 2.3 Implement tetromino movement methods (move, rotate_clockwise)
    - Implement immutable move operation returning new tetromino
    - Implement immutable rotate_clockwise operation
    - Implement get_absolute_blocks method for grid coordinate calculation
    - _Requirements: 3.1, 3.2, 3.3_
  
  - [ ] 2.4 Write property test for tetromino block count invariant
    - **Property 4: Tetromino Block Count Invariant**
    - **Validates: Requirements 2.1-2.8**
  
  - [ ] 2.5 Write property test for rotation preserves block count
    - **Property 6: Rotation Preserves Block Count**
    - **Validates: Requirements 3.3**
  
  - [ ] 2.6 Write property test for rotation center preservation
    - **Property 10: Rotation Center Preservation**
    - **Validates: Requirements 3.9**

- [ ] 3. Implement Playfield class for grid management
  - [ ] 3.1 Create Playfield class with 10×20 grid initialization
    - Initialize grid as 20 rows × 10 columns with None values
    - Implement get_cell and set_cell methods
    - _Requirements: 1.1, 1.4_
  
  - [ ] 3.2 Write property test for playfield dimensions invariant
    - **Property 1: Playfield Dimensions Invariant**
    - **Validates: Requirements 1.1**
  
  - [ ] 3.3 Write property test for playfield state accessibility
    - **Property 2: Playfield State Accessibility**
    - **Validates: Requirements 1.4**
  
  - [ ] 3.4 Implement collision detection methods
    - Implement is_valid_position to check if blocks fit within boundaries
    - Check for collisions with stopped blocks in the grid
    - _Requirements: 1.5, 1.6, 3.5, 3.6, 3.7_
  
  - [ ] 3.5 Write property test for boundary collision prevention
    - **Property 3: Boundary Collision Prevention**
    - **Validates: Requirements 1.5, 1.6, 3.5, 3.6**
  
  - [ ] 3.6 Write property test for collision detection correctness
    - **Property 8: Collision Detection Correctness**
    - **Validates: Requirements 3.7**
  
  - [ ] 3.7 Implement add_tetromino method to lock blocks into grid
    - Add tetromino blocks to grid with their colors
    - _Requirements: 4.3_
  
  - [ ] 3.8 Implement line clearing methods
    - Implement get_complete_rows to find fully occupied rows
    - Implement clear_rows to remove rows and shift blocks down
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ] 3.9 Write property test for complete row detection
    - **Property 13: Complete Row Detection**
    - **Validates: Requirements 5.1**
  
  - [ ] 3.10 Write property test for row clearing empties rows
    - **Property 14: Row Clearing Empties Rows**
    - **Validates: Requirements 5.2**
  
  - [ ] 3.11 Write property test for row clearing gravity
    - **Property 15: Row Clearing Gravity**
    - **Validates: Requirements 5.3, 5.5**
  
  - [ ] 3.12 Write property test for multiple row clearing
    - **Property 16: Multiple Row Clearing**
    - **Validates: Requirements 5.4**
  
  - [ ] 3.13 Implement is_game_over method
    - Check if any block exists in top row (y=0)
    - _Requirements: 7.1_

- [ ] 4. Checkpoint - Ensure core data structure tests pass
  - Run all tests for Tetromino and Playfield classes
  - Verify property tests pass with 100+ iterations
  - Ask the user if questions arise

- [ ] 5. Implement GameState class for game logic coordination
  - [ ] 5.1 Create GameState class with playfield, active tetromino, score, and game over flag
    - Initialize with empty playfield
    - Set up fall timer and fall interval (0.5 seconds)
    - _Requirements: 12.3, 12.4_
  
  - [ ] 5.2 Implement spawn_tetromino method
    - Randomly select one of seven tetromino types
    - Create tetromino at top center position (x=4, y=0)
    - Check for immediate collision (game over condition)
    - _Requirements: 4.4, 4.5_
  
  - [ ] 5.3 Write property test for post-lock spawning
    - **Property 12: Post-Lock Spawning**
    - **Validates: Requirements 4.4, 4.5**
  
  - [ ] 5.4 Implement movement methods (move_active_left, move_active_right, rotate_active)
    - Validate movement using playfield collision detection
    - Only update active tetromino if move is valid
    - Return boolean indicating success/failure
    - _Requirements: 3.1, 3.2, 3.3, 3.8_
  
  - [ ] 5.5 Write property test for movement delta correctness
    - **Property 5: Movement Delta Correctness**
    - **Validates: Requirements 3.1, 3.2**
  
  - [ ] 5.6 Write property test for rotation collision prevention
    - **Property 9: Rotation Collision Prevention**
    - **Validates: Requirements 3.8**
  
  - [ ] 5.7 Implement hard_drop method
    - Move active tetromino down until it collides
    - Immediately lock the tetromino
    - _Requirements: 3.4, 3.10, 3.11_
  
  - [ ] 5.8 Write property test for hard drop reaches bottom
    - **Property 7: Hard Drop Reaches Bottom**
    - **Validates: Requirements 3.4, 3.10**
  
  - [ ] 5.9 Implement lock_tetromino method
    - Add active tetromino blocks to playfield
    - Check for complete rows and clear them
    - Update score (4 points for lock + 10 per cleared row)
    - Spawn next tetromino
    - Check game over condition
    - _Requirements: 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 7.1_
  
  - [ ] 5.10 Write property test for tetromino locking adds blocks to playfield
    - **Property 11: Tetromino Locking Adds Blocks to Playfield**
    - **Validates: Requirements 4.1, 4.2, 4.3**
  
  - [ ] 5.11 Write property test for scoring monotonicity
    - **Property 17: Scoring Monotonicity**
    - **Validates: Requirements 6.4**
  
  - [ ] 5.12 Write property test for tetromino lock scoring
    - **Property 18: Tetromino Lock Scoring**
    - **Validates: Requirements 6.1**
  
  - [ ] 5.13 Write property test for line clear scoring
    - **Property 19: Line Clear Scoring**
    - **Validates: Requirements 6.2, 6.3**
  
  - [ ] 5.14 Write property test for game over detection
    - **Property 20: Game Over Detection**
    - **Validates: Requirements 7.1**
  
  - [ ] 5.15 Implement update method for automatic falling
    - Accumulate delta_time in fall_timer
    - When fall_timer exceeds fall_interval, move active tetromino down
    - Lock tetromino if it can't move down
    - Reset fall_timer after each automatic fall
    - _Requirements: 3.12, 12.3, 12.4, 12.5_
  
  - [ ] 5.16 Write property test for game over state immutability
    - **Property 21: Game Over State Immutability**
    - **Validates: Requirements 7.2, 7.3**

- [ ] 6. Checkpoint - Ensure game logic tests pass
  - Run all tests for GameState class
  - Verify all property tests pass
  - Test a complete game flow manually (spawn, move, lock, clear lines, game over)
  - Ask the user if questions arise

- [ ] 7. Implement HighScoreManager for persistence
  - [ ] 7.1 Create HighScoreEntry dataclass with name, score, and timestamp
    - Define dataclass with three fields
    - _Requirements: 9.3_
  
  - [ ] 7.2 Create HighScoreManager class with load and save methods
    - Initialize with file path (default: "high_scores.json")
    - Implement load method to read JSON file (handle missing file)
    - Implement save method to write JSON file
    - _Requirements: 8.2, 8.3, 8.7, 8.8_
  
  - [ ] 7.3 Write property test for high score persistence round-trip
    - **Property 23: High Score Persistence Round-Trip**
    - **Validates: Requirements 8.2, 8.3, 8.7, 9.4**
  
  - [ ] 7.4 Implement high score management methods
    - Implement is_high_score to check if score qualifies for top 10
    - Implement add_score to insert new score and maintain sorted order
    - Ensure list never exceeds 10 entries
    - _Requirements: 8.1, 8.4, 8.5, 8.6_
  
  - [ ] 7.5 Write property test for high score list size limit
    - **Property 22: High Score List Size Limit**
    - **Validates: Requirements 8.1**
  
  - [ ] 7.6 Write property test for high score qualification
    - **Property 24: High Score Qualification**
    - **Validates: Requirements 8.4**
  
  - [ ] 7.7 Write property test for high score addition
    - **Property 25: High Score Addition**
    - **Validates: Requirements 8.5**
  
  - [ ] 7.8 Write property test for high score sorting invariant
    - **Property 26: High Score Sorting Invariant**
    - **Validates: Requirements 8.6**
  
  - [ ] 7.9 Write property test for high score entry completeness
    - **Property 27: High Score Entry Completeness**
    - **Validates: Requirements 9.3**
  
  - [ ] 7.10 Write unit test for missing file edge case
    - Test that loading from non-existent file creates empty list
    - _Requirements: 8.8_

- [ ] 8. Implement Renderer class for Pygame graphics
  - [ ] 8.1 Create Renderer class with Pygame initialization
    - Initialize Pygame display (800×600 pixels)
    - Set up fonts for text rendering
    - Define color constants and block size (30 pixels)
    - _Requirements: 11.1, 11.2, 11.6_
  
  - [ ] 8.2 Implement playfield rendering methods
    - Implement render_grid_lines to draw playfield borders
    - Implement render_playfield to draw stopped blocks with colors
    - Calculate screen positions from grid coordinates
    - _Requirements: 11.2, 11.4_
  
  - [ ] 8.3 Implement tetromino rendering method
    - Implement render_tetromino to draw active tetromino blocks
    - Use tetromino's color for rendering
    - _Requirements: 11.3_
  
  - [ ] 8.4 Implement score rendering method
    - Implement render_score to display score at top of screen
    - _Requirements: 6.5_
  
  - [ ] 8.5 Implement render_game method to coordinate all rendering
    - Clear screen with background color
    - Call render_grid_lines, render_playfield, render_tetromino, render_score
    - Update Pygame display
    - _Requirements: 11.5, 11.7, 12.5_
  
  - [ ] 8.6 Write unit tests for rendering methods
    - Test that rendering methods don't crash with various game states
    - Use mock Pygame surfaces to avoid display requirements
    - _Requirements: 11.1-11.7_

- [ ] 9. Implement UIManager for screen management
  - [ ] 9.1 Create UIManager class with screen state enum
    - Define screen states: START, GAME, GAME_OVER, NAME_ENTRY, HIGH_SCORES
    - Initialize with START screen
    - _Requirements: 10.1_
  
  - [ ] 9.2 Implement start screen rendering
    - Display "TETRIS" title prominently
    - Display "Press SPACE to start" prompt
    - _Requirements: 10.2, 10.3_
  
  - [ ] 9.3 Implement game over screen rendering
    - Display "GAME OVER" message
    - Display final score
    - Display "Press SPACE to continue" prompt
    - _Requirements: 7.5, 10.7_
  
  - [ ] 9.4 Implement name entry screen rendering
    - Display "New High Score!" message
    - Display current score
    - Display text input field with current name
    - Display "Press ENTER to submit" prompt
    - _Requirements: 9.1, 9.2, 10.8_
  
  - [ ] 9.5 Implement high scores display screen rendering
    - Display "HIGH SCORES" title
    - Display top 10 scores with names in descending order
    - Display "Press SPACE to return" prompt
    - _Requirements: 9.5, 10.10_
  
  - [ ] 9.6 Implement screen transition logic
    - Implement transition methods between screens
    - Handle state changes based on game events
    - _Requirements: 10.4, 10.6_
  
  - [ ] 9.7 Write unit tests for UI screen transitions
    - Test START → GAME transition
    - Test GAME → GAME_OVER transition
    - Test GAME_OVER → NAME_ENTRY transition (when high score achieved)
    - Test NAME_ENTRY → HIGH_SCORES transition
    - _Requirements: 7.4, 9.1, 10.1, 10.4, 10.6, 10.8_

- [ ] 10. Implement InputHandler for keyboard processing
  - [ ] 10.1 Create InputHandler class with input processing methods
    - Implement handle_game_input for gameplay controls
    - Implement handle_menu_input for menu navigation
    - Implement handle_text_input for name entry
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ] 10.2 Implement game input mapping
    - Map LEFT ARROW to move_active_left
    - Map RIGHT ARROW to move_active_right
    - Map SPACE to rotate_active
    - Map DOWN ARROW to hard_drop
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ] 10.3 Implement menu and text input handling
    - Handle SPACE for menu selections
    - Handle character input and BACKSPACE for name entry
    - Handle ENTER to submit name
    - _Requirements: 9.3, 10.3_
  
  - [ ] 10.4 Write unit tests for input handling
    - Test that correct game state methods are called for each key
    - Test text input accumulation and submission
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 9.3_

- [ ] 11. Checkpoint - Ensure rendering and UI tests pass
  - Run all tests for Renderer, UIManager, and InputHandler
  - Verify rendering works with mock surfaces
  - Ask the user if questions arise

- [ ] 12. Implement main game loop
  - [ ] 12.1 Create main.py with game loop structure
    - Initialize Pygame
    - Create GameState, Renderer, UIManager, InputHandler, HighScoreManager instances
    - Implement main loop with event processing, state update, and rendering
    - _Requirements: 12.1, 12.2, 12.5_
  
  - [ ] 12.2 Implement frame timing and delta time calculation
    - Use Pygame clock to maintain consistent frame rate (60 FPS)
    - Calculate delta_time between frames
    - Pass delta_time to GameState.update for automatic falling
    - _Requirements: 11.5, 12.6_
  
  - [ ] 12.3 Implement event processing loop
    - Process Pygame events each frame
    - Route events to InputHandler based on current screen state
    - Handle QUIT event to exit game
    - _Requirements: 12.2_
  
  - [ ] 12.4 Implement screen-specific rendering
    - Render appropriate screen based on UIManager state
    - Render game screen during active gameplay
    - Render menu screens during non-gameplay states
    - _Requirements: 10.5, 11.7_
  
  - [ ] 12.5 Implement game over flow
    - Detect game over condition from GameState
    - Transition to game over screen
    - Check if score qualifies for high score list
    - Transition to name entry screen if high score achieved
    - Save high score after name entry
    - _Requirements: 7.2, 7.3, 7.4, 8.4, 8.5, 8.7, 9.1_
  
  - [ ] 12.6 Write integration tests for game loop
    - Test complete game flow from start to game over
    - Test high score flow when score qualifies
    - Test that game state doesn't change after game over
    - _Requirements: 7.1, 7.2, 7.3, 8.4, 8.5, 9.1_

- [ ] 13. Final testing and polish
  - [ ] 13.1 Run complete test suite
    - Run all unit tests and property tests
    - Verify all 27 properties pass with 100+ iterations
    - Fix any failing tests
  
  - [ ] 13.2 Manual gameplay testing
    - Play complete games to verify all mechanics work correctly
    - Test edge cases (clearing 4 rows simultaneously, game over at spawn)
    - Test high score persistence across game sessions
    - _Requirements: All_
  
  - [ ] 13.3 Add error handling and edge case handling
    - Add try-catch blocks for file I/O errors
    - Handle corrupted JSON gracefully
    - Add input validation for edge cases
    - _Requirements: 8.8_
  
  - [ ] 13.4 Add documentation and code comments
    - Add docstrings to all classes and methods
    - Add comments explaining complex logic (rotation, line clearing)
    - Update README with setup and run instructions

- [ ] 14. Final checkpoint - Complete implementation
  - Ensure all tests pass
  - Verify game runs smoothly with no crashes
  - Confirm high scores persist correctly
  - Ask the user if questions arise or if ready to deploy

## Notes

- All tasks are required for comprehensive correctness validation
- Each property test should run minimum 100 iterations using Hypothesis
- Property tests should be tagged with comments: `# Feature: tetris-clone, Property N: [title]`
- Core game logic (models/) should have no Pygame dependencies for easier testing
- Use temporary files for high score persistence tests to avoid polluting user data
- Consider using seeded random number generators in tests for reproducibility
