"""Task 6: Read text files and count words."""

from pathlib import Path


def count_words(filename):
    """Return the number of whitespace-separated words in a text file."""
    with open(filename, "r", encoding="utf-8") as file:
        contents = file.read()

    return len(contents.split())


if __name__ == "__main__":
    file_path = Path(__file__).resolve().parents[1] / "task6_read_me.txt"
    print(count_words(file_path))