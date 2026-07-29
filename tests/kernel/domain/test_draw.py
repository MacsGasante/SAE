from __future__ import annotations

from datetime import date

import pytest

from sae.kernel.collections import Combination
from sae.kernel.domain import Draw, DrawDate, DrawId
from sae.kernel.domain.exceptions import InvalidDrawError
from sae.kernel.foundation import Number


def build_combination() -> Combination:
    return Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )


def build_draw(draw_id: int = 1) -> Draw:
    return Draw(
        id=DrawId(draw_id),
        date=DrawDate.from_date(date(2026, 1, 7)),
        combination=build_combination(),
    )


def test_create_valid_draw() -> None:
    draw = build_draw()

    assert draw.id == DrawId(1)
    assert draw.date == DrawDate.from_date(date(2026, 1, 7))
    assert draw.combination == build_combination()


def test_numbers_property() -> None:
    draw = build_draw()

    assert draw.numbers == build_combination().numbers


def test_contains_existing_number() -> None:
    draw = build_draw()

    assert draw.contains(Number(4))


def test_contains_missing_number() -> None:
    draw = build_draw()

    assert not draw.contains(Number(90))


def test_invalid_draw_id() -> None:
    with pytest.raises(InvalidDrawError):
        Draw(
            id=1,  # type: ignore[arg-type]
            date=DrawDate.from_date(date.today()),
            combination=build_combination(),
        )


def test_invalid_draw_date() -> None:
    with pytest.raises(InvalidDrawError):
        Draw(
            id=DrawId(1),
            date=date.today(),  # type: ignore[arg-type]
            combination=build_combination(),
        )


def test_invalid_combination() -> None:
    with pytest.raises(InvalidDrawError):
        Draw(
            id=DrawId(1),
            date=DrawDate.from_date(date.today()),
            combination=(),  # type: ignore[arg-type]
        )


def test_same_id_is_equal() -> None:
    draw1 = build_draw(10)

    draw2 = Draw(
        id=DrawId(10),
        date=DrawDate.from_date(date(2030, 1, 1)),
        combination=Combination(
            Number(10),
            Number(20),
            Number(30),
            Number(40),
            Number(50),
            Number(60),
        ),
    )

    assert draw1 == draw2


def test_different_id_is_not_equal() -> None:
    assert build_draw(1) != build_draw(2)


def test_hashable() -> None:
    draws = {
        build_draw(1),
        build_draw(1),
    }

    assert len(draws) == 1


def test_repr_contains_draw() -> None:
    assert "Draw(" in repr(build_draw())


def test_numbers_are_delegated() -> None:
    draw = build_draw()

    assert draw.numbers is draw.combination.numbers
