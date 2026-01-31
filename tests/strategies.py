"""Custom Hypothesis strategies for property-based testing.

This module provides reusable strategies for generating test data for
Tetris game components including tetrominoes, playfields, game states,
and high scores.
"""

from datetime import datetime, timedelta
from hypothesis import strategies as st
from typing import List

from tetris.models.tetromino import Tetromino
from tetris.models.playfield import Playfield
from tetris.models.high_scores import HighScoreEntry


# ============================================================================
# Tetromino Strategies
# ============================================================================

def tetromino_type():
    """Strategy for generating valid tetromino types."""
    return st.sampled_from(['I', 'O', 'T', 'L', 'J', 'S', 'Z'])


def valid_rotation():
    """Strategy for generating valid rotation values."""
    return st.integers(min_value=0, max_value=3)


def valid_position():
    """Strategy for generating valid playfield positions."""
    return st.tuples(
        st.integers(min_value=0, max_value=9),   # x
        st.integers(min_value=0, max_value=19)   # y
    )


def tetromino():
    """Strategy for generating random tetrominoes."""
    return st.builds(
        Tetromino,
        shape_type=tetromino_type(),
        x=st.integers(min_value=-5, max_value=15),
        y=st.integers(min_value=-5, max_value=25),
        rotation=valid_rotation()
    )


# ============================================================================
# Playfield Strategies
# ============================================================================

def color():
    """Strategy for generating valid RGB color tuples."""
    return st.tuples(
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255)
    )


@st.composite
def playfield_with_blocks(draw):
    """Strategy for generating playfields with random stopped blocks."""
    playfield = Playfield()
    num_blocks = draw(st.integers(min_value=0, max_value=50))
    
    for _ in range(num_blocks):
        x = draw(st.integers(min_value=0, max_value=9))
        y = draw(st.integers(min_value=0, max_value=19))
        block_color = draw(color())
        playfield.set_cell(x, y, block_color)
    
    return playfield


# ============================================================================
# High Score Strategies
# ============================================================================

def player_name():
    """Strategy for generating valid player names."""
    return st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')),
        min_size=1,
        max_size=20
    )


def score_value():
    """Strategy for generating valid score values."""
    return st.integers(min_value=0, max_value=999999)


def timestamp_string():
    """Strategy for generating valid ISO format timestamp strings."""
    # Generate timestamps within the last year
    base_date = datetime.now()
    days_ago = st.integers(min_value=0, max_value=365)
    
    return st.builds(
        lambda days: (base_date - timedelta(days=days)).isoformat(),
        days_ago
    )


def high_score_entry():
    """Strategy for generating valid high score entries."""
    return st.builds(
        HighScoreEntry,
        name=player_name(),
        score=score_value(),
        timestamp=timestamp_string()
    )


def high_score_list(min_size=0, max_size=15):
    """Strategy for generating lists of high score entries.
    
    Args:
        min_size: Minimum number of entries (default: 0)
        max_size: Maximum number of entries (default: 15)
    """
    return st.lists(
        high_score_entry(),
        min_size=min_size,
        max_size=max_size
    )
