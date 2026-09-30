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


def test_from_official_creates_global_draw_id() -> None:
    draw_id = DrawId.from_official(
        year=2026,
        contest_number=155,
    )

    assert draw_id == DrawId(2026155)


def test_from_official_handles_first_contest_of_year() -> None:
    draw_id = DrawId.from_official(
        year=2026,
        contest_number=1,
    )

    assert draw_id == DrawId(2026001)


def test_from_official_is_deterministic() -> None:
    first = DrawId.from_official(
        year=2026,
        contest_number=155,
    )

    second = DrawId.from_official(
        year=2026,
        contest_number=155,
    )

    assert first == second
    assert first.value == second.value


def test_from_official_distinguishes_same_contest_number_across_years() -> None:
    previous_year = DrawId.from_official(
        year=2025,
        contest_number=1,
    )

    current_year = DrawId.from_official(
        year=2026,
        contest_number=1,
    )

    assert previous_year != current_year


def test_from_official_preserves_global_order_across_year_boundary() -> None:
    previous_year_last = DrawId.from_official(
        year=2025,
        contest_number=208,
    )

    current_year_first = DrawId.from_official(
        year=2026,
        contest_number=1,
    )

    assert previous_year_last < current_year_first


def test_from_official_preserves_order_within_year() -> None:
    first = DrawId.from_official(
        year=2026,
        contest_number=1,
    )

    later = DrawId.from_official(
        year=2026,
        contest_number=155,
    )

    assert first < later


@pytest.mark.parametrize(
    "year,contest_number",
    [
        (2026, 0),
        (2026, -1),
        (2025, 0),
        (2025, -10),
    ],
)
def test_from_official_rejects_invalid_contest_number(
    year: int,
    contest_number: int,
) -> None:
    with pytest.raises(InvalidDrawIdError):
        DrawId.from_official(
            year=year,
            contest_number=contest_number,
        )


@pytest.mark.parametrize(
    "year,contest_number",
    [
        (2026.0, 155),
        ("2026", 155),
        (None, 155),
        (2026, 155.0),
        (2026, "155"),
        (2026, None),
        (True, 155),
        (2026, True),
    ],
)
def test_from_official_rejects_invalid_types(
    year: object,
    contest_number: object,
) -> None:
    with pytest.raises(InvalidDrawIdError):
        DrawId.from_official(
            year=year,  # type: ignore[arg-type]
            contest_number=contest_number,  # type: ignore[arg-type]
        )


def test_from_official_rejects_contest_number_outside_global_id_range() -> None:
    with pytest.raises(InvalidDrawIdError):
        DrawId.from_official(
            year=2026,
            contest_number=1000,
        )
