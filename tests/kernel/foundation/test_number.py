from __future__ import annotations

import pytest

from sae.kernel.exceptions import InvalidNumberError
from sae.kernel.foundation.number import Number


def test_create_valid_number() -> None:
    number = Number(42)

    assert number.value == 42
    assert number.to_int() == 42


@pytest.mark.parametrize("value", [1, 25, 90])
def test_valid_boundary_values(value: int) -> None:
    number = Number(value)

    assert number.value == value


@pytest.mark.parametrize("value", [0, -1, 91, 100])
def test_invalid_range(value: int) -> None:
    with pytest.raises(InvalidNumberError):
        Number(value)


@pytest.mark.parametrize(
    "value",
    [
        7.5,
        "7",
        None,
        [],
        {},
        object(),
    ],
)
def test_invalid_type(value: object) -> None:
    with pytest.raises(InvalidNumberError):
        Number(value)  # type: ignore[arg-type]


def test_equality() -> None:
    assert Number(17) == Number(17)
    assert Number(17) != Number(18)


def test_ordering() -> None:
    assert Number(5) < Number(12)
    assert Number(90) > Number(1)


def test_hashability() -> None:
    values = {Number(5), Number(5), Number(8)}

    assert len(values) == 2


def test_string_representation() -> None:
    number = Number(7)

    assert str(number) == "7"
    assert repr(number) == "Number(7)"
