"""Tests for Task 3 control structures."""

import pytest

from src.task3 import (
    classify_number,
    first_ten_primes,
    sum_one_to_one_hundred,
)


@pytest.mark.parametrize(
    "number, expected",
    [
        (5, "positive"),
        (-5, "negative"),
        (0, "zero"),
        (0.001, "positive"),
        (-0.001, "negative"),
        (1000000, "positive"),
        (-1000000, "negative"),
    ],
)
def test_classify_number(number, expected):
    """Test positive, negative, zero, and edge-case values."""
    assert classify_number(number) == expected


def test_first_ten_primes():
    """Test that the first ten prime numbers are correct."""
    assert first_ten_primes() == [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
    ]


def test_sum_one_to_one_hundred():
    """Test the sum of all integers from 1 through 100."""
    assert sum_one_to_one_hundred() == 5050