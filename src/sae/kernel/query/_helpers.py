"""
Shared query helpers.

Private helper functions shared by the Query Layer.

This module contains only pure functions.
"""

from __future__ import annotations

from collections.abc import Callable

from sae.kernel.dataset import Dataset
from sae.kernel.domain import Draw


def select(
    dataset: Dataset,
    predicate: Callable[[Draw], bool],
) -> Dataset:
    """
    Return a Dataset containing every Draw satisfying the predicate.

    Fundamental filtering primitive of the Query Layer.
    """
    return Dataset(draw for draw in dataset.draws if predicate(draw))
