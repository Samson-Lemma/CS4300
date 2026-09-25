"""Tests for Task 5 lists and dictionaries."""

import pytest

from src.task5 import (
    favorite_books,
    first_three_books,
    get_student_id,
    student_database,
)


def test_first_three_books():
    """Test that list slicing returns the first three books."""
    assert first_three_books() == favorite_books[:3]
    assert len(first_three_books()) == 3


def test_student_database():
    """Test the student names and IDs stored in the dictionary."""
    assert student_database["Alice"] == 1001
    assert student_database["Bob"] == 1002
    assert student_database["Charlie"] == 1003


def test_get_student_id():
    """Test looking up an existing student's ID."""
    assert get_student_id("Alice") == 1001


def test_missing_student():
    """Test that looking up an unknown student raises KeyError."""
    with pytest.raises(KeyError):
        get_student_id("Unknown Student")