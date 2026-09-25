"""Tests for Task 6 file handling."""

from pathlib import Path

import pytest

from src.task6 import count_words


@pytest.mark.parametrize(
    "contents, expected",
    [
        ("Hello world", 2),
        ("one two three four", 4),
        ("", 0),
        ("Python\nis\na\nprogramming\nlanguage", 5),
        ("   extra    spaces   here   ", 3),
    ],
)
def test_count_words(tmp_path, contents, expected):
    """Test word counting using several temporary text files."""
    file_path = tmp_path / "test.txt"
    file_path.write_text(contents, encoding="utf-8")

    assert count_words(file_path) == expected


def test_missing_file():
    """Test that a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        count_words("does_not_exist.txt")


def test_assignment_file():
    """Test the exact word count of the assignment text file."""
    file_path = Path(__file__).resolve().parents[1] / "task6_read_me.txt"

    assert count_words(file_path) == 104