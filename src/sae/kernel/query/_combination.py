"""
Combination query functions.

Private functions implementing combination-based Dataset queries.
"""

from __future__ import annotations

from sae.kernel.collections import Combination
from sae.kernel.dataset import Dataset
from sae.kernel.foundation.constants import COMBINATION_SIZE

from ._helpers import select


def _validate_at_least(
    at_least: int,
) -> None:
    """
    Validate the minimum number of required matches.

    Valid values are between 1 and COMBINATION_SIZE inclusive.
    """
    if not 1 <= at_least <= COMBINATION_SIZE:
        raise ValueError(f"at_least must be between 1 and {COMBINATION_SIZE}.")


def _filter_matches(
    dataset: Dataset,
    combination: Combination,
    *,
    at_least: int,
) -> Dataset:
    """
    Return Draws matching at least `at_least` Numbers.
    """
    _validate_at_least(at_least)

    return select(
        dataset,
        lambda draw: (
            draw.matches(
                combination,
            ).count
            >= at_least
        ),
    )


def contains_exactly(
    dataset: Dataset,
    combination: Combination,
) -> Dataset:
    """
    Return Draws matching every Number in the Combination.
    """
    return _filter_matches(
        dataset,
        combination,
        at_least=len(combination),
    )


def intersects(
    dataset: Dataset,
    combination: Combination,
) -> Dataset:
    """
    Return Draws sharing at least one Number.
    """
    return _filter_matches(
        dataset,
        combination,
        at_least=1,
    )


def matches(
    dataset: Dataset,
    combination: Combination,
    *,
    at_least: int,
) -> Dataset:
    """
    Return Draws matching at least `at_least` Numbers.
    """
    return _filter_matches(
        dataset,
        combination,
        at_least=at_least,
    )
