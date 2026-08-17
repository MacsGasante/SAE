"""
Number Query Functions.

Pure functions implementing Dataset queries based on Number objects.
"""

from __future__ import annotations

from sae.kernel.dataset import Dataset
from sae.kernel.foundation import Number

from ._helpers import select


def by_number(
    dataset: Dataset,
    number: Number,
) -> Dataset:
    """
    Return every Draw containing the given Number.
    """
    return select(
        dataset,
        lambda draw: number in draw.combination,
    )


def contains(
    dataset: Dataset,
    number: Number,
) -> Dataset:
    """
    Alias of by_number().

    Improves readability in fluent queries.
    """
    return by_number(
        dataset,
        number,
    )


def contains_any(
    dataset: Dataset,
    *numbers: Number,
) -> Dataset:
    """
    Return every Draw containing at least one Number.
    """
    return select(
        dataset,
        lambda draw: any(number in draw.combination for number in numbers),
    )


def contains_all(
    dataset: Dataset,
    *numbers: Number,
) -> Dataset:
    """
    Return every Draw containing all Numbers.
    """
    return select(
        dataset,
        lambda draw: all(number in draw.combination for number in numbers),
    )
