"""Task 5: Demonstrate lists, slicing, and dictionaries."""


favorite_books = [
    ("The Hobbit", "J.R.R. Tolkien"),
    ("Dune", "Frank Herbert"),
    ("1984", "George Orwell"),
    ("The Martian", "Andy Weir"),
    ("Fahrenheit 451", "Ray Bradbury"),
]


student_database = {
    "Alice": 1001,
    "Bob": 1002,
    "Charlie": 1003,
}


def first_three_books():
    """Return the first three books using list slicing."""
    return favorite_books[:3]


def get_student_id(name):
    """Return the student ID associated with a student name."""
    return student_database[name]


if __name__ == "__main__":
    print(first_three_books())
    print(student_database)