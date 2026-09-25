from src.task5 import (
    favorite_books,
    first_three_books,
    get_student_id,
    student_database,
)


def test_first_three_books():
    assert first_three_books() == favorite_books[:3]
    assert len(first_three_books()) == 3


def test_student_database():
    assert student_database["Alice"] == 1001
    assert student_database["Bob"] == 1002
    assert student_database["Charlie"] == 1003


def test_get_student_id():
    assert get_student_id("Alice") == 1001