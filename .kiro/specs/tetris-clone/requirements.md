# Requirements Document: Tetris Clone

## Introduction

This document specifies the requirements for a classic Tetris clone game implemented in Python using Pygame. The game features traditional Tetris gameplay mechanics including falling tetrominoes, line clearing, scoring, and a high score system with local persistence.

## Glossary

- **Game_Engine**: The core system managing game state, logic, and coordination
- **Playfield**: The 10×20 grid where tetrominoes fall and accumulate
- **Tetromino**: A geometric shape composed of four square blocks
- **Active_Tetromino**: The currently falling tetromino under player control
- **Stopped_Tetromino**: A tetromino that has landed and become part of the playfield
- **Complete_Row**: A horizontal row in the playfield with all 10 positions occupied
- **Input_Handler**: The system processing keyboard input from the player
- **Renderer**: The system responsible for drawing graphics to the screen
- **Score_Manager**: The system tracking and calculating player score
- **High_Score_System**: The system managing persistent high score storage and retrieval
- **UI_Manager**: The system managing user interface screens and transitions

## Requirements

### Requirement 1: Playfield Structure

**User Story:** As a player, I want a clearly defined playing area, so that I understand the game boundaries and can plan my moves.

#### Acceptance Criteria

1. THE Playfield SHALL consist of exactly 10 columns and 20 rows
2. THE Playfield SHALL represent each position as a square block of equal size
3. THE Playfield SHALL maintain a portrait orientation (height greater than width)
4. THE Playfield SHALL track the state of each position (empty or occupied with color)
5. THE Playfield SHALL prevent Active_Tetromino movement beyond the left boundary
6. THE Playfield SHALL prevent Active_Tetromino movement beyond the right boundary

### Requirement 2: Tetromino Shapes and Properties

**User Story:** As a player, I want seven distinct tetromino shapes with unique colors, so that I can easily identify and differentiate them during gameplay.

#### Acceptance Criteria

1. THE Game_Engine SHALL support exactly seven tetromino types (I, L, J, O, S, Z, T)
2. THE I_Tetromino SHALL be a 1×4 straight line with light blue color
3. THE L_Tetromino SHALL be 3 blocks high and 2 blocks wide extending right with orange color
4. THE J_Tetromino SHALL be 3 blocks high and 2 blocks wide extending left with dark blue color
5. THE O_Tetromino SHALL be a 2×2 square with yellow color
6. THE S_Tetromino SHALL be 3 blocks wide with 2 upper blocks and 2 lower blocks offset right with green color
7. THE Z_Tetromino SHALL be 3 blocks wide with 2 upper blocks and 2 lower blocks offset left with red color
8. THE T_Tetromino SHALL be 3 blocks wide and 2 blocks high in T-shape with purple color
9. WHEN a Tetromino is created, THE Game_Engine SHALL assign it the correct shape configuration and color

### Requirement 3: Tetromino Movement and Control

**User Story:** As a player, I want to control falling tetrominoes with keyboard inputs, so that I can position and rotate them strategically.

#### Acceptance Criteria

1. WHEN the left arrow key is pressed, THE Input_Handler SHALL move the Active_Tetromino one column left
2. WHEN the right arrow key is pressed, THE Input_Handler SHALL move the Active_Tetromino one column right
3. WHEN the space key is pressed, THE Input_Handler SHALL rotate the Active_Tetromino 90 degrees clockwise
4. WHEN the down arrow key is pressed, THE Input_Handler SHALL immediately drop the Active_Tetromino until it lands
5. IF the Active_Tetromino would collide with the left boundary, THEN THE Game_Engine SHALL prevent leftward movement
6. IF the Active_Tetromino would collide with the right boundary, THEN THE Game_Engine SHALL prevent rightward movement
7. IF the Active_Tetromino would collide with Stopped_Tetromino blocks, THEN THE Game_Engine SHALL prevent movement in that direction
8. IF a rotation would cause collision with boundaries or Stopped_Tetromino blocks, THEN THE Game_Engine SHALL prevent the rotation
9. WHEN rotating, THE Game_Engine SHALL maintain the center position of the Active_Tetromino
10. WHEN the down arrow key is pressed, THE Active_Tetromino SHALL move downward continuously until landing
11. WHEN the Active_Tetromino lands from a hard drop, THE Game_Engine SHALL immediately convert it to a Stopped_Tetromino
12. THE Game_Engine SHALL continuously move the Active_Tetromino downward at a moderate constant speed during normal falling

### Requirement 4: Tetromino Landing and Spawning

**User Story:** As a player, I want tetrominoes to stop when they land and new ones to appear, so that gameplay continues smoothly.

#### Acceptance Criteria

1. WHEN the Active_Tetromino touches the bottom of the Playfield, THE Game_Engine SHALL convert it to a Stopped_Tetromino
2. WHEN the Active_Tetromino touches any Stopped_Tetromino block below it, THE Game_Engine SHALL convert it to a Stopped_Tetromino
3. WHEN a Tetromino becomes a Stopped_Tetromino, THE Game_Engine SHALL add its blocks to the Playfield state
4. WHEN a Tetromino becomes a Stopped_Tetromino, THE Game_Engine SHALL spawn a new Active_Tetromino at the top center of the Playfield
5. WHEN spawning a new Tetromino, THE Game_Engine SHALL randomly select one of the seven tetromino types

### Requirement 5: Line Clearing Mechanics

**User Story:** As a player, I want completed rows to be cleared and the structure to drop down, so that I can continue playing and prevent the playfield from filling up.

#### Acceptance Criteria

1. WHEN a Tetromino becomes a Stopped_Tetromino, THE Game_Engine SHALL check all rows for completion
2. WHEN a Complete_Row is detected, THE Game_Engine SHALL remove all blocks from that row
3. WHEN a Complete_Row is removed, THE Game_Engine SHALL move all rows above it down by one position
4. WHEN multiple Complete_Rows exist, THE Game_Engine SHALL clear all of them and adjust the playfield accordingly
5. THE Game_Engine SHALL preserve the color and position of blocks when moving rows downward

### Requirement 6: Scoring System

**User Story:** As a player, I want to earn points for placing tetrominoes and clearing lines, so that I can track my performance and compete for high scores.

#### Acceptance Criteria

1. WHEN a Tetromino becomes a Stopped_Tetromino, THE Score_Manager SHALL award points equal to the number of blocks in that tetromino (4 points)
2. WHEN a Complete_Row is cleared, THE Score_Manager SHALL award a bonus of 10 points per cleared row
3. WHEN multiple rows are cleared simultaneously, THE Score_Manager SHALL award the bonus for each cleared row
4. THE Score_Manager SHALL maintain a running total of the player's score during gameplay
5. THE Renderer SHALL display the current score at the top of the game screen

### Requirement 7: Game Over Condition

**User Story:** As a player, I want the game to end when tetrominoes reach the top, so that I know when I've lost and can see my final score.

#### Acceptance Criteria

1. WHEN a Stopped_Tetromino has any block in the top row of the Playfield, THE Game_Engine SHALL trigger game over
2. WHEN game over is triggered, THE Game_Engine SHALL stop spawning new tetrominoes
3. WHEN game over is triggered, THE Game_Engine SHALL stop accepting player input for tetromino control
4. WHEN game over is triggered, THE UI_Manager SHALL transition to the game over screen
5. WHEN the game over screen is displayed, THE UI_Manager SHALL show the player's final score

### Requirement 8: High Score Persistence

**User Story:** As a player, I want my high scores to be saved locally, so that I can track my best performances across game sessions.

#### Acceptance Criteria

1. THE High_Score_System SHALL maintain a list of the top 10 scores
2. THE High_Score_System SHALL store high scores in a JSON file in the local file system
3. WHEN the game starts, THE High_Score_System SHALL load existing high scores from the JSON file
4. WHEN a game ends, THE High_Score_System SHALL check if the final score qualifies for the top 10
5. IF the final score qualifies for top 10, THEN THE High_Score_System SHALL add it to the high score list
6. WHEN a new high score is added, THE High_Score_System SHALL maintain the list sorted in descending order
7. WHEN a new high score is added, THE High_Score_System SHALL save the updated list to the JSON file
8. IF the high score file does not exist, THEN THE High_Score_System SHALL create it with an empty list

### Requirement 9: High Score Name Entry

**User Story:** As a player, I want to enter my name when I achieve a high score, so that my accomplishment is properly attributed.

#### Acceptance Criteria

1. WHEN a player achieves a top 10 score, THE UI_Manager SHALL prompt the player to enter their name
2. THE UI_Manager SHALL provide a text input interface for name entry
3. WHEN the player submits their name, THE High_Score_System SHALL associate it with the score
4. THE High_Score_System SHALL store both the score and the player name in the JSON file
5. WHEN displaying high scores, THE UI_Manager SHALL show both the player name and score for each entry

### Requirement 10: User Interface Screens

**User Story:** As a player, I want clear navigation between start, game, and game over screens, so that I have a polished gaming experience.

#### Acceptance Criteria

1. WHEN the game application launches, THE UI_Manager SHALL display the start screen
2. THE Start_Screen SHALL display the title "TETRIS" prominently
3. THE Start_Screen SHALL provide a start button or key prompt to begin gameplay
4. WHEN the player activates the start button, THE UI_Manager SHALL transition to the game screen
5. THE Game_Screen SHALL display the Playfield, current score, and Active_Tetromino
6. WHEN game over is triggered, THE UI_Manager SHALL transition to the game over screen
7. THE Game_Over_Screen SHALL display the final score
8. WHERE the player achieved a top 10 score, THE Game_Over_Screen SHALL display the name entry interface
9. THE Game_Over_Screen SHALL provide an option to view the high score list
10. THE High_Score_Display SHALL show all top 10 scores with player names in descending order

### Requirement 11: Graphics Rendering

**User Story:** As a player, I want clear and simple 2D graphics, so that I can easily see the game state and focus on gameplay.

#### Acceptance Criteria

1. THE Renderer SHALL use Pygame library for graphics rendering
2. THE Renderer SHALL draw each block in the Playfield as a filled square with its assigned color
3. THE Renderer SHALL draw the Active_Tetromino with its designated color
4. THE Renderer SHALL draw grid lines or borders to clearly delineate the Playfield boundaries
5. THE Renderer SHALL update the display at a consistent frame rate (minimum 30 FPS)
6. THE Renderer SHALL draw text elements (score, title, buttons) with readable fonts
7. WHEN a Tetromino becomes a Stopped_Tetromino, THE Renderer SHALL immediately reflect the change in the display

### Requirement 12: Game Loop and Timing

**User Story:** As a player, I want smooth and consistent gameplay timing, so that the game feels responsive and fair.

#### Acceptance Criteria

1. THE Game_Engine SHALL implement a game loop that runs continuously during active gameplay
2. THE Game_Engine SHALL process player input every frame
3. THE Game_Engine SHALL move the Active_Tetromino downward at fixed time intervals
4. THE Game_Engine SHALL maintain a consistent fall speed throughout a game session
5. THE Game_Engine SHALL update game state before rendering each frame
6. THE Game_Engine SHALL handle frame timing to maintain consistent gameplay speed across different hardware
