"""High score management and persistence.

This module provides functionality for managing and persisting high scores
to a JSON file. It maintains a sorted list of the top 10 scores with player
names and timestamps.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class HighScoreEntry:
    """Represents a single high score entry.
    
    Attributes:
        name: Player name (non-empty string)
        score: Score value (non-negative integer)
        timestamp: ISO format timestamp string of when the score was achieved
    """
    name: str
    score: int
    timestamp: str
    
    def __post_init__(self) -> None:
        """Validate high score entry fields."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.score, int) or self.score < 0:
            raise ValueError("Score must be a non-negative integer")
        if not isinstance(self.timestamp, str):
            raise ValueError("Timestamp must be a string")


class HighScoreManager:
    """Manages high score persistence and ranking.
    
    Maintains a list of the top 10 high scores, sorted in descending order
    by score value. Provides methods to load/save scores from/to a JSON file,
    check if a score qualifies for the top 10, and add new scores.
    
    Attributes:
        file_path: Path to the JSON file for persistence
        scores: List of HighScoreEntry objects, sorted by score descending
    """
    
    MAX_SCORES = 10
    
    def __init__(self, file_path: str = "high_scores.json") -> None:
        """Initialize the high score manager.
        
        Args:
            file_path: Path to the JSON file for storing high scores
        """
        self.file_path = file_path
        self.scores: List[HighScoreEntry] = []
        self.load()
    
    def load(self) -> None:
        """Load high scores from the JSON file.
        
        If the file doesn't exist, initializes with an empty list.
        If the file is corrupted, logs a warning and initializes with an empty list.
        """
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.scores = [HighScoreEntry(**entry) for entry in data]
        except FileNotFoundError:
            # First run - no high scores yet
            self.scores = []
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Corrupted file or invalid data - log and start fresh
            print(f"Warning: Corrupted high score file: {e}")
            self.scores = []
    
    def save(self) -> None:
        """Save high scores to the JSON file.
        
        Writes the current scores list to the JSON file. If unable to write,
        logs an error but allows the program to continue.
        """
        try:
            with open(self.file_path, 'w') as f:
                data = [asdict(entry) for entry in self.scores]
                json.dump(data, f, indent=2)
        except (IOError, OSError) as e:
            # Write permission error - log but continue
            print(f"Error: Unable to save high scores: {e}")
    
    def is_high_score(self, score: int) -> bool:
        """Check if a score qualifies for the top 10.
        
        Args:
            score: The score value to check
            
        Returns:
            True if the score qualifies for the top 10, False otherwise
        """
        if len(self.scores) < self.MAX_SCORES:
            return True
        return score > self.scores[-1].score
    
    def add_score(self, name: str, score: int) -> None:
        """Add a new high score entry.
        
        Adds the score if it qualifies for the top 10, maintains the list
        sorted in descending order, and ensures the list never exceeds 10 entries.
        
        Args:
            name: Player name
            score: Score value
        """
        if not self.is_high_score(score):
            return
        
        # Create new entry with current timestamp
        timestamp = datetime.now().isoformat()
        entry = HighScoreEntry(name=name, score=score, timestamp=timestamp)
        
        # Add to list and sort
        self.scores.append(entry)
        self.scores.sort(key=lambda e: e.score, reverse=True)
        
        # Keep only top 10
        self.scores = self.scores[:self.MAX_SCORES]
    
    def get_top_scores(self, n: int = MAX_SCORES) -> List[HighScoreEntry]:
        """Get the top N high scores.
        
        Args:
            n: Number of scores to return (default: 10)
            
        Returns:
            List of up to N high score entries, sorted by score descending
        """
        return self.scores[:n]
