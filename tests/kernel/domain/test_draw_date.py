from __future__ import annotations

from datetime import date

import pytest

from sae.kernel.domain import DrawDate
from sae.kernel.domain.exceptions import InvalidDrawDateError


def test_create_valid_draw_date() -> None:
    draw_date = DrawDate.from_ymd(2026, 8, 5)

    assert draw_date.year == 2026
    assert draw_date.month == 8
    assert draw_date.day == 5


def test_from_date() -> None:
    value = date(2025, 12, 25)

    draw_date = DrawDate.from_date(value)

    assert draw_date.to_date() == value


def test_isoformat() -> None:
    draw_date = DrawDate.from_ymd(2026, 1, 15)

    assert draw_date.isoformat() == "2026-01-15"


@pytest.mark.parametrize(
    "year,month,day",
    [
        (2023, 2, 29),
        (2024, 13, 1),
        (2024, 0, 1),
        (2024, 1, 32),
        (2024, 1, 0),
    ],
)
def test_invalid_calendar_dates(
    year: int,
    month: int,
    day: int,
) -> None:
    with pytest.raises(InvalidDrawDateError):
        DrawDate.from_ymd(year, month, day)


def test_ordering() -> None:
    assert DrawDate.from_ymd(2024, 1, 1) < DrawDate.from_ymd(2025, 1, 1)


def test_hashability() -> None:
    values = {
        DrawDate.from_ymd(2024, 1, 1),
        DrawDate.from_ymd(2024, 1, 1),
    }

    assert len(values) == 1


def test_repr() -> None:
    value = DrawDate.from_ymd(2024, 6, 15)

    assert repr(value) == "DrawDate(2024-06-15)"


def test_datetime_is_rejected() -> None:
    from datetime import datetime

    with pytest.raises(InvalidDrawDateError):
        DrawDate(datetime(2026, 8, 5, 12, 30))


def test_str() -> None:
    value = DrawDate.from_ymd(2024, 6, 15)

    assert str(value) == "2024-06-15"


def test_from_ymd_is_alias_of_from_parts() -> None:
    assert DrawDate.from_ymd(2024, 6, 15) == DrawDate.from_parts(
        2024,
        6,
        15,
    )
