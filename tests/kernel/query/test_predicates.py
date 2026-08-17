"""
Dataset query predicate tests.
"""

from __future__ import annotations

from sae.kernel.domain import DrawDate, DrawId
from sae.kernel.query._predicates import (
    after,
    all_of,
    any_of,
    before,
    between,
    by_day,
    by_draw_id,
    by_month,
    by_year,
    negate,
)
from tests.kernel.types import DrawFactory


def test_before_matches_only_earlier_draws(
    make_draw: DrawFactory,
) -> None:
    """
    before matches draws strictly before the given date.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = before(
        DrawDate.from_ymd(
            2024,
            1,
            2,
        )
    )

    assert predicate(draw) is True


def test_before_excludes_equal_date(
    make_draw: DrawFactory,
) -> None:
    """
    before excludes draws on the given date.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = before(
        DrawDate.from_ymd(
            2024,
            1,
            1,
        )
    )

    assert predicate(draw) is False


def test_after_matches_only_later_draws(
    make_draw: DrawFactory,
) -> None:
    """
    after matches draws strictly after the given date.
    """
    draw = make_draw(
        1,
        2024,
        1,
        2,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = after(
        DrawDate.from_ymd(
            2024,
            1,
            1,
        )
    )

    assert predicate(draw) is True


def test_after_excludes_equal_date(
    make_draw: DrawFactory,
) -> None:
    """
    after excludes draws on the given date.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = after(
        DrawDate.from_ymd(
            2024,
            1,
            1,
        )
    )

    assert predicate(draw) is False


def test_between_includes_start_and_end_dates(
    make_draw: DrawFactory,
) -> None:
    """
    between uses a closed interval.
    """
    draw_start = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    draw_end = make_draw(
        2,
        2024,
        1,
        3,
        (10, 11, 12, 13, 14, 15),
    )

    predicate = between(
        DrawDate.from_ymd(
            2024,
            1,
            1,
        ),
        DrawDate.from_ymd(
            2024,
            1,
            3,
        ),
    )

    assert predicate(draw_start) is True
    assert predicate(draw_end) is True


def test_between_excludes_dates_outside_interval(
    make_draw: DrawFactory,
) -> None:
    """
    between excludes draws outside the closed interval.
    """
    draw = make_draw(
        1,
        2024,
        1,
        4,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = between(
        DrawDate.from_ymd(
            2024,
            1,
            1,
        ),
        DrawDate.from_ymd(
            2024,
            1,
            3,
        ),
    )

    assert predicate(draw) is False


def test_by_year_matches_draw_year(
    make_draw: DrawFactory,
) -> None:
    """
    by_year matches draws belonging to the requested year.
    """
    draw = make_draw(
        1,
        2024,
        6,
        15,
        (1, 2, 3, 4, 5, 6),
    )

    assert by_year(2024)(draw) is True
    assert by_year(2025)(draw) is False


def test_by_month_matches_draw_month(
    make_draw: DrawFactory,
) -> None:
    """
    by_month matches draws belonging to the requested month.
    """
    draw = make_draw(
        1,
        2024,
        6,
        15,
        (1, 2, 3, 4, 5, 6),
    )

    assert by_month(6)(draw) is True
    assert by_month(7)(draw) is False


def test_by_day_matches_draw_day(
    make_draw: DrawFactory,
) -> None:
    """
    by_day matches draws belonging to the requested day.
    """
    draw = make_draw(
        1,
        2024,
        6,
        15,
        (1, 2, 3, 4, 5, 6),
    )

    assert by_day(15)(draw) is True
    assert by_day(16)(draw) is False


def test_by_draw_id_matches_draw_identifier(
    make_draw: DrawFactory,
) -> None:
    """
    by_draw_id matches draws with the requested DrawId.
    """
    draw = make_draw(
        42,
        2024,
        6,
        15,
        (1, 2, 3, 4, 5, 6),
    )

    assert (
        by_draw_id(
            DrawId(42),
        )(draw)
        is True
    )

    assert (
        by_draw_id(
            DrawId(43),
        )(draw)
        is False
    )


def test_negate_reverses_predicate_result(
    make_draw: DrawFactory,
) -> None:
    """
    negate reverses the result of another predicate.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = by_year(2024)

    assert negate(predicate)(draw) is False
    assert negate(negate(predicate))(draw) is True


def test_all_of_requires_all_predicates(
    make_draw: DrawFactory,
) -> None:
    """
    all_of implements logical AND.
    """
    draw = make_draw(
        1,
        2024,
        6,
        15,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = all_of(
        by_year(2024),
        by_month(6),
        by_day(15),
    )

    assert predicate(draw) is True

    predicate = all_of(
        by_year(2024),
        by_month(7),
    )

    assert predicate(draw) is False


def test_any_of_requires_at_least_one_predicate(
    make_draw: DrawFactory,
) -> None:
    """
    any_of implements logical OR.
    """
    draw = make_draw(
        1,
        2024,
        6,
        15,
        (1, 2, 3, 4, 5, 6),
    )

    predicate = any_of(
        by_year(2025),
        by_month(6),
    )

    assert predicate(draw) is True

    predicate = any_of(
        by_year(2025),
        by_month(7),
    )

    assert predicate(draw) is False


def test_all_of_without_predicates_is_true(
    make_draw: DrawFactory,
) -> None:
    """
    all_of with no predicates follows all() semantics.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    assert all_of()(draw) is True


def test_any_of_without_predicates_is_false(
    make_draw: DrawFactory,
) -> None:
    """
    any_of with no predicates follows any() semantics.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    assert any_of()(draw) is False
