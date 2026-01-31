---
inclusion: always
---

# Project Context: Tetris Clone

## Project Overview

This is a learning project to understand Kiro IDE's spec-driven development approach. The goal is to implement a complete, working Tetris clone in Python using Pygame, following best practices for testing, architecture, and code quality.

## Project Goals

### Primary Goals
1. **Learn spec-driven development**: Experience the requirements → design → tasks → implementation workflow
2. **Build a complete game**: Fully functional Tetris with all classic features
3. **Practice property-based testing**: Use Hypothesis to verify correctness properties
4. **Write clean, maintainable code**: Follow architectural patterns and coding standards

### Non-Goals
- Performance optimization (it's a simple game)
- Advanced graphics or animations
- Multiplayer or networking
- Mobile or web deployment

## Technology Stack

### Core Technologies
- **Language**: Python 3.8+
- **Graphics**: Pygame (simple 2D graphics library)
- **Testing**: pytest (unit tests) + Hypothesis (property-based tests)
- **Persistence**: JSON files (for high scores)

### Why These Choices?
- **Python**: Easy to learn, great for prototyping, excellent testing tools
- **Pygame**: Simple API, perfect for 2D games, well-documented
- **Hypothesis**: Powerful property-based testing, finds edge cases automatically
- **JSON**: Simple, human-readable, no database needed

## Development Workflow

### Spec-Driven Approach
1. **Requirements**: Define what the system should do (acceptance criteria)
2. **Design**: Define how it will work (architecture, correctness properties)
3. **Tasks**: Break down implementation into steps
4. **Implementation**: Execute tasks one at a time
5. **Testing**: Verify with unit tests and property tests

### Task Execution Flow
1. Pick a task from tasks.md
2. Implement the code following steering file guidelines
3. Write tests (unit + property tests as specified)
4. Run tests and verify they pass
5. Mark task complete
6. Move to next task

### Checkpoints
The task list includes checkpoints to pause and verify:
- After core data structures (Tetromino, Playfield)
- After game logic (GameState)
- After rendering and UI
- Before final completion

## Project Structure

### Directory Layout
```
try-out-project/
├── .kiro/
│   ├── specs/
│   │   └── tetris-clone/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   └── steering/
│       ├── architecture-patterns.md
│       ├── python-standards.md
│       ├── testing-practices.md
│       ├── pygame-patterns.md
│       └── project-context.md
├── tetris/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── views/
│   └── controllers/
├── tests/
│   └── (test files)
├── requirements.txt
├── high_scores.json (created at runtime)
└── README.md
```

### Key Files
- **requirements.txt**: Python dependencies (pygame, hypothesis, pytest)
- **main.py**: Entry point, runs the game
- **high_scores.json**: Persistent high score storage (created automatically)

## Development Principles

### Code Quality Over Speed
- Take time to write clean, well-tested code
- Follow the steering file guidelines
- Don't skip tests to "move faster"
- Refactor when code becomes unclear

### Test-Driven Mindset
- Write tests as you implement features
- Run tests frequently
- Fix failing tests immediately
- Aim for high coverage (90%+)

### Incremental Progress
- Complete one task at a time
- Don't jump ahead to "interesting" tasks
- Build foundation before adding features
- Verify at checkpoints

### Learning Focus
- Understand WHY, not just WHAT
- Ask questions when unclear
- Experiment and explore
- Document lessons learned

## Common Patterns in This Project

### Immutable Tetrominoes
Tetromino operations return new instances:
```python
moved = tetromino.move(1, 0)  # Returns new tetromino
rotated = tetromino.rotate_clockwise()  # Returns new tetromino
```

### GameState Coordination
GameState orchestrates all game logic:
```python
game_state.move_active_left()  # Validates and moves if possible
game_state.update(delta_time)  # Handles automatic falling
game_state.lock_tetromino()    # Locks, clears lines, updates score
```

### Separation of Concerns
- Models: Pure logic, no Pygame
- Views: Pure rendering, no logic
- Controllers: Pure routing, no logic

### Property-Based Testing
Each correctness property has a test:
```python
@given(tetromino=tetromino())
def test_property_4_block_count(tetromino):
    """Property 4: Any tetromino has exactly 4 blocks."""
    assert len(tetromino.get_absolute_blocks()) == 4
```

## Expected Challenges

### Challenge 1: Rotation Logic
Tetromino rotation can be tricky, especially near boundaries.

**Solution**: Pre-calculate all rotation states, test thoroughly with property tests

### Challenge 2: Line Clearing
Clearing multiple rows and shifting blocks down correctly.

**Solution**: Clear from bottom to top, test with property tests for gravity

### Challenge 3: Collision Detection
Detecting collisions with boundaries and stopped blocks.

**Solution**: Separate boundary checks from block checks, test exhaustively

### Challenge 4: Game Loop Timing
Maintaining consistent frame rate and fall speed.

**Solution**: Use delta time, Pygame clock, test timing logic separately

## Success Criteria

### Minimum Viable Product
- [ ] All 7 tetromino shapes work correctly
- [ ] Pieces fall, move, rotate as expected
- [ ] Lines clear when complete
- [ ] Score tracks correctly
- [ ] Game ends when pieces reach top
- [ ] High scores persist across sessions

### Quality Criteria
- [ ] All 27 correctness properties pass
- [ ] 90%+ test coverage
- [ ] No Pygame in models/
- [ ] Clean, documented code
- [ ] Follows all steering file guidelines

### Learning Criteria
- [ ] Understand spec-driven workflow
- [ ] Comfortable with property-based testing
- [ ] Can explain architectural decisions
- [ ] Can extend the game with new features

## Next Steps After Completion

### Possible Extensions
Once the core game is complete, consider:
- **Difficulty levels**: Increase fall speed over time
- **Next piece preview**: Show upcoming tetromino
- **Hold piece**: Allow holding one piece for later
- **Scoring variations**: Combo bonuses, T-spin detection
- **Visual polish**: Animations, particle effects
- **Sound effects**: Add audio feedback

### Applying to Real Projects
Use this experience to:
- Apply spec-driven approach to work projects
- Use property-based testing for critical logic
- Follow architectural patterns for maintainability
- Create steering files for team standards

## Resources

### Documentation
- Pygame docs: https://www.pygame.org/docs/
- Hypothesis docs: https://hypothesis.readthedocs.io/
- pytest docs: https://docs.pytest.org/

### Tetris Reference
- Tetris guidelines: https://tetris.wiki/Tetris_Guideline
- Rotation systems: https://tetris.wiki/SRS

### Kiro IDE
- Spec-driven development: See this project as example
- Steering files: See .kiro/steering/ for examples
- Property-based testing: See design.md for property definitions

## Notes and Observations

### What's Working Well
(To be filled in during development)

### Challenges Encountered
(To be filled in during development)

### Lessons Learned
(To be filled in during development)

### Ideas for Improvement
(To be filled in during development)

---

**Remember**: This is a learning project. The goal is not just to build Tetris, but to understand and practice professional software development workflows. Take your time, ask questions, and enjoy the process!
