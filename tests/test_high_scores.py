"""Unit tests for the HighScoreManager class.

This module tests high score persistence, ranking, and management.
It includes both specific example-based tests and property-based tests using Hypothesis.
"""

import json
import os
import tempfile
from datetime import datetime
from typing import List

import pytest
from hypothesis import given, settings, strategies as st

from tetris.models.high_scores import HighScoreEntry, HighScoreManager
from tests.strategies import high_score_entry, high_score_list, player_name, score_value


# ============================================================================
# Fixtures
# ============================================================================

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
def high_score_manager(temp_high_score_file):
    """Provide a fresh high score manager with temporary file."""
    return HighScoreManager(file_path=temp_high_score_file)


# ============================================================================
# Unit Tests - HighScoreEntry
# ============================================================================

class TestHighScoreEntry:
    """Test HighScoreEntry dataclass."""
    
    def test_create_high_score_entry(self):
        """Test creating a valid high score entry."""
        timestamp = datetime.now().isoformat()
        entry = HighScoreEntry(name="Alice", score=1000, timestamp=timestamp)
        
        assert entry.name == "Alice"
        assert entry.score == 1000
        assert entry.timestamp == timestamp
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        timestamp = datetime.now().isoformat()
        with pytest.raises(ValueError, match="non-empty string"):
            HighScoreEntry(name="", score=1000, timestamp=timestamp)
    
    def test_negative_score_raises_error(self):
        """Test that negative score raises ValueError."""
        timestamp = datetime.now().isoformat()
        with pytest.raises(ValueError, match="non-negative integer"):
            HighScoreEntry(name="Bob", score=-100, timestamp=timestamp)
    
    def test_non_string_timestamp_raises_error(self):
        """Test that non-string timestamp raises ValueError."""
        with pytest.raises(ValueError, match="must be a string"):
            HighScoreEntry(name="Charlie", score=500, timestamp=12345)


# ============================================================================
# Unit Tests - HighScoreManager Initialization
# ============================================================================

class TestHighScoreManagerInit:
    """Test HighScoreManager initialization."""
    
    def test_create_manager_with_default_path(self):
        """Test creating manager with default file path."""
        manager = HighScoreManager()
        assert manager.file_path == "high_scores.json"
        assert isinstance(manager.scores, list)
    
    def test_create_manager_with_custom_path(self, temp_high_score_file):
        """Test creating manager with custom file path."""
        manager = HighScoreManager(file_path=temp_high_score_file)
        assert manager.file_path == temp_high_score_file
        assert isinstance(manager.scores, list)
    
    def test_max_scores_constant(self):
        """Test that MAX_SCORES is set to 10."""
        assert HighScoreManager.MAX_SCORES == 10


# ============================================================================
# Unit Tests - Load and Save
# ============================================================================

class TestLoadAndSave:
    """Test loading and saving high scores."""
    
    def test_load_from_nonexistent_file(self, temp_high_score_file):
        """Test loading from non-existent file creates empty list."""
        # Remove the temp file
        os.remove(temp_high_score_file)
        
        manager = HighScoreManager(file_path=temp_high_score_file)
        assert manager.scores == []
    
    def test_save_and_load_single_score(self, high_score_manager):
        """Test saving and loading a single score."""
        high_score_manager.add_score("Alice", 1000)
        high_score_manager.save()
        
        # Load in new instance
        manager2 = HighScoreManager(file_path=high_score_manager.file_path)
        assert len(manager2.scores) == 1
        assert manager2.scores[0].name == "Alice"
        assert manager2.scores[0].score == 1000
    
    def test_save_and_load_multiple_scores(self, high_score_manager):
        """Test saving and loading multiple scores."""
        high_score_manager.add_score("Alice", 1000)
        high_score_manager.add_score("Bob", 800)
        high_score_manager.add_score("Charlie", 1200)
        high_score_manager.save()
        
        # Load in new instance
        manager2 = HighScoreManager(file_path=high_score_manager.file_path)
        assert len(manager2.scores) == 3
        # Should be sorted descending
        assert manager2.scores[0].score == 1200
        assert manager2.scores[1].score == 1000
        assert manager2.scores[2].score == 800
    
    def test_load_corrupted_json(self, temp_high_score_file):
        """Test loading corrupted JSON file."""
        # Write invalid JSON
        with open(temp_high_score_file, 'w') as f:
            f.write("{ invalid json }")
        
        # Should handle gracefully
        manager = HighScoreManager(file_path=temp_high_score_file)
        assert manager.scores == []


# ============================================================================
# Unit Tests - High Score Management
# ============================================================================

class TestHighScoreManagement:
    """Test high score management methods."""
    
    def test_is_high_score_empty_list(self, high_score_manager):
        """Test that any score qualifies when list is empty."""
        assert high_score_manager.is_high_score(0)
        assert high_score_manager.is_high_score(100)
        assert high_score_manager.is_high_score(1000)
    
    def test_is_high_score_partial_list(self, high_score_manager):
        """Test qualification when list has fewer than 10 entries."""
        for i in range(5):
            high_score_manager.add_score(f"Player{i}", (5 - i) * 100)
        
        # Any score should qualify (list not full)
        assert high_score_manager.is_high_score(0)
        assert high_score_manager.is_high_score(1000)
    
    def test_is_high_score_full_list(self, high_score_manager):
        """Test qualification when list is full."""
        # Fill with scores 100, 200, ..., 1000
        for i in range(10):
            high_score_manager.add_score(f"Player{i}", (10 - i) * 100)
        
        # Score must beat lowest (100)
        assert not high_score_manager.is_high_score(50)
        assert not high_score_manager.is_high_score(100)
        assert high_score_manager.is_high_score(101)
        assert high_score_manager.is_high_score(500)
    
    def test_add_score_to_empty_list(self, high_score_manager):
        """Test adding score to empty list."""
        high_score_manager.add_score("Alice", 1000)
        
        assert len(high_score_manager.scores) == 1
        assert high_score_manager.scores[0].name == "Alice"
        assert high_score_manager.scores[0].score == 1000
    
    def test_add_score_maintains_sort_order(self, high_score_manager):
        """Test that adding scores maintains descending order."""
        high_score_manager.add_score("Alice", 500)
        high_score_manager.add_score("Bob", 1000)
        high_score_manager.add_score("Charlie", 750)
        
        assert high_score_manager.scores[0].score == 1000
        assert high_score_manager.scores[1].score == 750
        assert high_score_manager.scores[2].score == 500
    
    def test_add_score_limits_to_10(self, high_score_manager):
        """Test that list never exceeds 10 entries."""
        # Add 15 scores
        for i in range(15):
            high_score_manager.add_score(f"Player{i}", (15 - i) * 100)
        
        assert len(high_score_manager.scores) == 10
        # Should keep top 10
        assert high_score_manager.scores[0].score == 1500
        assert high_score_manager.scores[9].score == 600
    
    def test_add_non_qualifying_score(self, high_score_manager):
        """Test that non-qualifying score is not added."""
        # Fill with high scores
        for i in range(10):
            high_score_manager.add_score(f"Player{i}", (10 - i) * 1000)
        
        initial_count = len(high_score_manager.scores)
        
        # Try to add low score
        high_score_manager.add_score("Loser", 500)
        
        # Should not be added
        assert len(high_score_manager.scores) == initial_count
        assert all(entry.name != "Loser" for entry in high_score_manager.scores)
    
    def test_get_top_scores_default(self, high_score_manager):
        """Test getting top scores with default parameter."""
        for i in range(15):
            high_score_manager.add_score(f"Player{i}", (15 - i) * 100)
        
        top_scores = high_score_manager.get_top_scores()
        assert len(top_scores) == 10
    
    def test_get_top_scores_custom_n(self, high_score_manager):
        """Test getting top N scores."""
        for i in range(10):
            high_score_manager.add_score(f"Player{i}", (10 - i) * 100)
        
        top_5 = high_score_manager.get_top_scores(5)
        assert len(top_5) == 5
        assert top_5[0].score == 1000
        assert top_5[4].score == 600
    
    def test_timestamp_is_set(self, high_score_manager):
        """Test that timestamp is automatically set when adding score."""
        before = datetime.now()
        high_score_manager.add_score("Alice", 1000)
        after = datetime.now()
        
        entry = high_score_manager.scores[0]
        timestamp = datetime.fromisoformat(entry.timestamp)
        
        assert before <= timestamp <= after


# ============================================================================
# Property-Based Tests
# ============================================================================

class TestHighScoreProperties:
    """Property-based tests for high score invariants."""
    
    @settings(max_examples=100)
    @given(scores=high_score_list(min_size=1, max_size=10))
    def test_property_23_high_score_persistence_round_trip(self, scores):
        """Property 23: Saving and loading preserves high score list.
        
        Feature: tetris-clone, Property 23: High Score Persistence Round-Trip
        Validates: Requirements 8.2, 8.3, 8.7, 9.4
        """
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            # Create manager and manually set scores
            manager1 = HighScoreManager(file_path=temp_path)
            manager1.scores = scores
            manager1.save()
            
            # Load in new instance
            manager2 = HighScoreManager(file_path=temp_path)
            
            # Verify same number of entries
            assert len(manager2.scores) == len(scores), (
                f"Expected {len(scores)} entries, got {len(manager2.scores)}"
            )
            
            # Verify each entry matches
            for i, (original, loaded) in enumerate(zip(scores, manager2.scores)):
                assert loaded.name == original.name, (
                    f"Entry {i}: name mismatch - expected {original.name}, got {loaded.name}"
                )
                assert loaded.score == original.score, (
                    f"Entry {i}: score mismatch - expected {original.score}, got {loaded.score}"
                )
                assert loaded.timestamp == original.timestamp, (
                    f"Entry {i}: timestamp mismatch"
                )
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @settings(max_examples=100)
    @given(scores=high_score_list(min_size=0, max_size=15))
    def test_property_22_high_score_list_size_limit(self, scores):
        """Property 22: High score list never exceeds 10 entries.
        
        Feature: tetris-clone, Property 22: High Score List Size Limit
        Validates: Requirements 8.1
        """
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            manager = HighScoreManager(file_path=temp_path)
            
            # Add all scores
            for entry in scores:
                manager.add_score(entry.name, entry.score)
            
            # Verify list size
            assert len(manager.scores) <= 10, (
                f"High score list has {len(manager.scores)} entries, maximum is 10"
            )
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @settings(max_examples=100)
    @given(
        existing_scores=high_score_list(min_size=0, max_size=10),
        new_score=score_value()
    )
    def test_property_24_high_score_qualification(self, existing_scores, new_score):
        """Property 24: Score qualifies if list not full or beats lowest score.
        
        Feature: tetris-clone, Property 24: High Score Qualification
        Validates: Requirements 8.4
        """
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            manager = HighScoreManager(file_path=temp_path)
            manager.scores = sorted(existing_scores, key=lambda e: e.score, reverse=True)
            
            qualifies = manager.is_high_score(new_score)
            
            if len(manager.scores) < 10:
                # List not full - any score qualifies
                assert qualifies, (
                    f"Score {new_score} should qualify when list has {len(manager.scores)} entries"
                )
            else:
                # List full - must beat lowest score
                lowest_score = manager.scores[-1].score
                expected_qualifies = new_score > lowest_score
                assert qualifies == expected_qualifies, (
                    f"Score {new_score} qualification incorrect: "
                    f"expected {expected_qualifies}, got {qualifies} "
                    f"(lowest score: {lowest_score})"
                )
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @settings(max_examples=100)
    @given(
        existing_scores=high_score_list(min_size=0, max_size=9),
        name=player_name(),
        score=score_value()
    )
    def test_property_25_high_score_addition(self, existing_scores, name, score):
        """Property 25: Adding qualifying score maintains list properties.
        
        Feature: tetris-clone, Property 25: High Score Addition
        Validates: Requirements 8.5
        """
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            manager = HighScoreManager(file_path=temp_path)
            manager.scores = list(existing_scores)
            
            initial_count = len(manager.scores)
            
            # Add score (should qualify since list not full)
            manager.add_score(name, score)
            
            # Verify entry was added
            assert len(manager.scores) == initial_count + 1, (
                f"Expected {initial_count + 1} entries, got {len(manager.scores)}"
            )
            
            # Verify list doesn't exceed 10
            assert len(manager.scores) <= 10, (
                f"List has {len(manager.scores)} entries, maximum is 10"
            )
            
            # Verify new entry is in the list
            assert any(e.name == name and e.score == score for e in manager.scores), (
                f"New entry ({name}, {score}) not found in list"
            )
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @settings(max_examples=100)
    @given(scores=high_score_list(min_size=2, max_size=15))
    def test_property_26_high_score_sorting_invariant(self, scores):
        """Property 26: High score list is always sorted descending by score.
        
        Feature: tetris-clone, Property 26: High Score Sorting Invariant
        Validates: Requirements 8.6
        """
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            manager = HighScoreManager(file_path=temp_path)
            
            # Add scores in random order
            for entry in scores:
                manager.add_score(entry.name, entry.score)
            
            # Verify sorted in descending order
            for i in range(len(manager.scores) - 1):
                assert manager.scores[i].score >= manager.scores[i + 1].score, (
                    f"Scores not sorted: position {i} has score {manager.scores[i].score}, "
                    f"position {i+1} has score {manager.scores[i+1].score}"
                )
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @settings(max_examples=100)
    @given(scores=high_score_list(min_size=1, max_size=10))
    def test_property_27_high_score_entry_completeness(self, scores):
        """Property 27: All high score entries have valid name and score.
        
        Feature: tetris-clone, Property 27: High Score Entry Completeness
        Validates: Requirements 9.3
        """
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            manager = HighScoreManager(file_path=temp_path)
            
            # Add all scores
            for entry in scores:
                manager.add_score(entry.name, entry.score)
            
            # Verify all entries are complete
            for i, entry in enumerate(manager.scores):
                assert isinstance(entry.name, str) and len(entry.name) > 0, (
                    f"Entry {i} has invalid name: {entry.name}"
                )
                assert isinstance(entry.score, int) and entry.score >= 0, (
                    f"Entry {i} has invalid score: {entry.score}"
                )
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
