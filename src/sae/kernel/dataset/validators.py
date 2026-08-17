"""
Dataset validation utilities.

Contains the invariant validation logic used by Dataset.
"""

from __future__ import annotations

from collections.abc import Iterable
from operator import attrgetter

from ..domain import Draw, DrawDate, DrawId
from .exceptions import InvalidDatasetError


def normalize_draws(
    draws: Iterable[Draw],
) -> tuple[Draw, ...]:
    """
    Normalize draws into an immutable chronologically ordered tuple.
    """
    normalized = tuple(draws)

    for draw in normalized:
        validate_draw_type(draw)

    return tuple(
        sorted(
            normalized,
            key=attrgetter("date"),
        )
    )


def validate_dataset(
    draws: tuple[Draw, ...],
) -> None:
    """
    Validate every Dataset invariant.
    """
    ids: set[DrawId] = set()
    dates: set[DrawDate] = set()

    for draw in draws:
        validate_draw_type(draw)
        validate_draw_id(draw, ids)
        validate_draw_date(draw, dates)


def validate_draw_type(
    draw: Draw,
) -> None:
    """
    Validate Draw type.
    """
    if not isinstance(draw, Draw):
        raise InvalidDatasetError("Dataset accepts only Draw instances.")


def validate_draw_id(
    draw: Draw,
    ids: set[DrawId],
) -> None:
    """
    Validate DrawId uniqueness.
    """
    if draw.id in ids:
        raise InvalidDatasetError("Duplicate DrawId values are not allowed.")

    ids.add(draw.id)


def validate_draw_date(
    draw: Draw,
    dates: set[DrawDate],
) -> None:
    """
    Validate DrawDate uniqueness.
    """
    if draw.date in dates:
        raise InvalidDatasetError("Duplicate DrawDate values are not allowed.")

    dates.add(draw.date)
