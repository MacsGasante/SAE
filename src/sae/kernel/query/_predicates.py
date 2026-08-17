"""
Dataset query predicates.

Reusable predicates used by DatasetQuery.
"""

from __future__ import annotations

from collections.abc import Callable

from sae.kernel.domain import Draw, DrawDate, DrawId

DrawPredicate = Callable[[Draw], bool]


#
# ----------------------------------------------------------------------
# Date predicates
# ----------------------------------------------------------------------
#


def before(
    date: DrawDate,
) -> DrawPredicate:
    """
    Match draws strictly before the given date.
    """
    return lambda draw: draw.date < date


def after(
    date: DrawDate,
) -> DrawPredicate:
    """
    Match draws strictly after the given date.
    """
    return lambda draw: draw.date > date


def between(
    start: DrawDate,
    end: DrawDate,
) -> DrawPredicate:
    """
    Match draws inside the closed interval.

    start <= draw.date <= end
    """
    return lambda draw: start <= draw.date <= end


#
# ----------------------------------------------------------------------
# Calendar predicates
# ----------------------------------------------------------------------
#


def by_year(
    year: int,
) -> DrawPredicate:
    """
    Match every draw belonging to the given year.
    """
    return lambda draw: draw.date.year == year


def by_month(
    month: int,
) -> DrawPredicate:
    """
    Match every draw belonging to the given month.
    """
    return lambda draw: draw.date.month == month


def by_day(
    day: int,
) -> DrawPredicate:
    """
    Match every draw belonging to the given day of month.
    """
    return lambda draw: draw.date.day == day


#
# ----------------------------------------------------------------------
# Identity predicates
# ----------------------------------------------------------------------
#


def by_draw_id(
    identifier: DrawId,
) -> DrawPredicate:
    """
    Match a Draw by identifier.
    """
    return lambda draw: draw.id == identifier


#
# ----------------------------------------------------------------------
# Predicate combinators
# ----------------------------------------------------------------------
#


def negate(
    predicate: DrawPredicate,
) -> DrawPredicate:
    """
    Logical NOT.
    """
    return lambda draw: not predicate(draw)


def all_of(
    *predicates: DrawPredicate,
) -> DrawPredicate:
    """
    Logical AND.
    """
    return lambda draw: all(predicate(draw) for predicate in predicates)


def any_of(
    *predicates: DrawPredicate,
) -> DrawPredicate:
    """
    Logical OR.
    """
    return lambda draw: any(predicate(draw) for predicate in predicates)
