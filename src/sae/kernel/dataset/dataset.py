"""
Dataset Aggregate Root.

Represents the complete immutable historical archive of
SuperEnalotto draws.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..domain import Draw
from ..foundation.base import AggregateRoot
from .exceptions import InvalidDatasetError
from .protocol import DatasetProtocolMixin
from .validators import normalize_draws, validate_dataset

if TYPE_CHECKING:
    from sae.kernel.query import DatasetQuery


@dataclass(frozen=True, slots=True, init=False)
class Dataset(
    DatasetProtocolMixin,
    AggregateRoot,
):
    """
    Aggregate Root representing the complete historical archive.

    The Dataset guarantees:

    - immutable storage;
    - unique Draw identifiers;
    - unique Draw dates;
    - chronological ordering.
    """

    _draws: tuple[Draw, ...]

    def __init__(
        self,
        draws: Iterable[Draw],
    ) -> None:
        """
        Create a Dataset from an iterable of Draw objects.
        """
        normalized = normalize_draws(draws)

        validate_dataset(normalized)

        object.__setattr__(
            self,
            "_draws",
            normalized,
        )

    @property
    def draws(self) -> tuple[Draw, ...]:
        """
        Return the immutable collection of draws.
        """
        return self._draws

    @property
    def size(self) -> int:
        """
        Return the number of draws.
        """
        return len(self._draws)

    @property
    def count(self) -> int:
        """
        Return the number of draws.

        This property is an alias of ``size`` provided for
        readability in client code.
        """
        return self.size

    @property
    def is_empty(self) -> bool:
        """
        Return True if the Dataset contains no draws.
        """
        return not self._draws

    @property
    def first(self) -> Draw:
        """
        Return the oldest draw.

        Raises
        ------
        InvalidDatasetError
            If the Dataset is empty.
        """
        if not self._draws:
            raise InvalidDatasetError("Dataset is empty.")

        return self._draws[0]

    @property
    def last(self) -> Draw:
        """
        Return the most recent draw.

        Raises
        ------
        InvalidDatasetError
            If the Dataset is empty.
        """
        if not self._draws:
            raise InvalidDatasetError("Dataset is empty.")

        return self._draws[-1]

    @property
    def query(self) -> DatasetQuery:
        """
        Return the Dataset query facade.
        """
        from sae.kernel.query import DatasetQuery

        return DatasetQuery(self)

    def __repr__(self) -> str:
        """
        Return the developer representation of the Dataset.
        """
        if self._draws:
            return (
                "Dataset("
                f"size={self.size}, "
                f"first={self._draws[0].id}, "
                f"last={self._draws[-1].id}"
                ")"
            )

        return "Dataset(size=0)"

    def filter(
        self,
        predicate: Callable[[Draw], bool],
    ) -> Dataset:
        """
        Return a new Dataset containing only draws matching
        the given predicate.

        Backward-compatible facade delegating to DatasetQuery.
        """
        return self.query.filter(predicate).dataset
