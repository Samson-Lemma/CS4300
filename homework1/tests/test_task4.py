import pytest

from src.task4 import calculate_discount


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 20, 80),
        (100.0, 20, 80.0),
        (50, 10.5, 44.75),
        (49.99, 10, 44.991),
        (100, 0, 100),
        (100, 100, 0),
    ],
)
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == pytest.approx(expected)


@pytest.mark.parametrize(
    "price, discount",
    [
        (-100, 10),
        (100, -1),
        (100, 101),
    ],
)
def test_invalid_values(price, discount):
    with pytest.raises(ValueError):
        calculate_discount(price, discount)