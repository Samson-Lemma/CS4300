import pytest

from src.task2 import get_data_types


@pytest.mark.parametrize(
    "index, expected_type, expected_value",
    [
        (0, int, 42),
        (1, float, 3.14),
        (2, str, "Python"),
        (3, bool, True),
    ],
)
def test_data_types(index, expected_type, expected_value):
    values = get_data_types()

    assert isinstance(values[index], expected_type)
    assert values[index] == expected_value