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
    file_path = tmp_path / "test.txt"
    file_path.write_text(contents, encoding="utf-8")

    assert count_words(file_path) == expected


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        count_words("does_not_exist.txt")


def test_assignment_file():
    assert count_words("task6_read_me.txt") > 0