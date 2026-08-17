"""
Dataset selection utilities.

Pure functions used by Dataset fluent operations.
"""

from __future__ import annotations

from collections.abc import Callable

from ..domain import Draw, DrawDate


def take(
    draws: tuple[Draw, ...],
    count: int,
) -> tuple[Draw, ...]:
    """
    Return the first count draws.
    """
    if count <= 0:
        return ()

    if count >= len(draws):
        return draws

    return draws[:count]


def skip(
    draws: tuple[Draw, ...],
    count: int,
) -> tuple[Draw, ...]:
    """
    Skip the first count draws.
    """
    if count <= 0:
        return draws

    if count >= len(draws):
        return ()

    return draws[count:]


def filter_draws(
    draws: tuple[Draw, ...],
    predicate: Callable[[Draw], bool],
) -> tuple[Draw, ...]:
    """
    Return every draw satisfying the predicate.
    """
    return tuple(draw for draw in draws if predicate(draw))


def before(
    draws: tuple[Draw, ...],
    date: DrawDate,
) -> tuple[Draw, ...]:
    """
    Return every draw before the given date.
    """
    return filter_draws(
        draws,
        lambda draw: draw.date < date,
    )


def after(
    draws: tuple[Draw, ...],
    date: DrawDate,
) -> tuple[Draw, ...]:
    """
    Return every draw after the given date.
    """
    return filter_draws(
        draws,
        lambda draw: draw.date > date,
    )


def between(
    draws: tuple[Draw, ...],
    start: DrawDate,
    end: DrawDate,
) -> tuple[Draw, ...]:
    """
    Return every draw in the closed interval.
    """
    return filter_draws(
        draws,
        lambda draw: start <= draw.date <= end,
    )
