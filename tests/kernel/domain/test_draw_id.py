from __future__ import annotations

import pytest

from sae.kernel.domain.draw_id import DrawId
from sae.kernel.domain.exceptions import InvalidDrawIdError


def test_create_valid_draw_id() -> None:
    draw_id = DrawId(1)

    assert draw_id.value == 1


@pytest.mark.parametrize(
    "value",
    [
        1,
        25,
        100,
        999999,
    ],
)
def test_valid_values(value: int) -> None:
    draw_id = DrawId(value)

    assert draw_id.value == value


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        -100,
    ],
)
def test_invalid_range(value: int) -> None:
    with pytest.raises(InvalidDrawIdError):
        DrawId(value)


@pytest.mark.parametrize(
    "value",
    [
        2.5,
        "10",
        None,
        [],
        {},
        object(),
    ],
)
def test_invalid_type(value: object) -> None:
    with pytest.raises(InvalidDrawIdError):
        DrawId(value)  # type: ignore[arg-type]


def test_to_int_returns_underlying_value() -> None:
    draw_id = DrawId(123)

    assert draw_id.to_int() == 123


def test_equality() -> None:
    assert DrawId(100) == DrawId(100)

    assert DrawId(100) != DrawId(101)


def test_ordering() -> None:
    assert DrawId(1) < DrawId(2)


def test_hashability() -> None:
    draw_ids = {
        DrawId(1),
        DrawId(2),
        DrawId(1),
    }

    assert len(draw_ids) == 2
    assert DrawId(1) in draw_ids
    assert DrawId(2) in draw_ids


def test_str_returns_numeric_value() -> None:
    draw_id = DrawId(123)

    assert str(draw_id) == "123"


def test_repr_returns_debug_representation() -> None:
    draw_id = DrawId(123)

    assert repr(draw_id) == "DrawId(123)"


def test_bool_is_rejected() -> None:
    with pytest.raises(InvalidDrawIdError):
        DrawId(True)
