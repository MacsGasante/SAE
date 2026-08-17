"""
Dataset Query Facade.

Provides the fluent public API used to query a Dataset.

The facade contains no business logic.
Every operation delegates to pure query functions.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from sae.kernel.collections import Combination
from sae.kernel.domain import Draw, DrawDate, DrawId
from sae.kernel.foundation import Number

from ._combination import (
    contains_exactly,
    intersects,
    matches,
)
from ._helpers import select
from ._number import (
    by_number,
    contains,
    contains_all,
    contains_any,
)
from ._predicates import (
    after as after_predicate,
)
from ._predicates import (
    before as before_predicate,
)
from ._predicates import (
    between as between_predicate,
)
from ._predicates import (
    by_day as by_day_predicate,
)
from ._predicates import (
    by_draw_id as by_draw_id_predicate,
)
from ._predicates import (
    by_month as by_month_predicate,
)
from ._predicates import (
    by_year as by_year_predicate,
)

if TYPE_CHECKING:
    from sae.kernel.dataset import Dataset


class DatasetQuery:
    """
    Fluent query facade for Dataset.

    Every method returns a new DatasetQuery wrapping
    the resulting Dataset.
    """

    __slots__ = ("_dataset",)

    def __init__(
        self,
        dataset: Dataset,
    ) -> None:
        self._dataset = dataset

    @classmethod
    def _wrap(
        cls,
        dataset: Dataset,
    ) -> DatasetQuery:
        """
        Wrap a Dataset in a new DatasetQuery.
        """
        return cls(dataset)

    def _select(
        self,
        predicate: Callable[[Draw], bool],
    ) -> DatasetQuery:
        """
        Select draws matching a predicate and wrap the result.
        """
        return self._wrap(
            select(
                self._dataset,
                predicate,
            )
        )

    @property
    def dataset(self) -> Dataset:
        """
        Return the Dataset associated with this query facade.
        """
        return self._dataset

    # ------------------------------------------------------------------
    # Date selection
    # ------------------------------------------------------------------

    def before(
        self,
        date: DrawDate,
    ) -> DatasetQuery:
        """
        Return draws strictly before the given date.
        """
        return self._select(
            before_predicate(date),
        )

    def after(
        self,
        date: DrawDate,
    ) -> DatasetQuery:
        """
        Return draws strictly after the given date.
        """
        return self._select(
            after_predicate(date),
        )

    def between(
        self,
        start: DrawDate,
        end: DrawDate,
    ) -> DatasetQuery:
        """
        Return draws inside the closed date interval.
        """
        return self._select(
            between_predicate(
                start,
                end,
            ),
        )

    # ------------------------------------------------------------------
    # Temporal queries
    # ------------------------------------------------------------------

    def by_year(
        self,
        year: int,
    ) -> DatasetQuery:
        """
        Return draws belonging to the given year.
        """
        return self._select(
            by_year_predicate(year),
        )

    def by_month(
        self,
        month: int,
    ) -> DatasetQuery:
        """
        Return draws belonging to the given month.
        """
        return self._select(
            by_month_predicate(month),
        )

    def by_day(
        self,
        day: int,
    ) -> DatasetQuery:
        """
        Return draws belonging to the given day of month.
        """
        return self._select(
            by_day_predicate(day),
        )

    def by_draw_id(
        self,
        identifier: DrawId,
    ) -> DatasetQuery:
        """
        Return the draw matching the given DrawId.
        """
        return self._select(
            by_draw_id_predicate(identifier),
        )

    # ------------------------------------------------------------------
    # Number queries
    # ------------------------------------------------------------------

    def by_number(
        self,
        number: Number,
    ) -> DatasetQuery:
        """
        Return draws containing the given Number.
        """
        return self._wrap(
            by_number(
                self._dataset,
                number,
            )
        )

    def contains(
        self,
        number: Number,
    ) -> DatasetQuery:
        """
        Return draws containing the given Number.
        """
        return self._wrap(
            contains(
                self._dataset,
                number,
            )
        )

    def contains_any(
        self,
        *numbers: Number,
    ) -> DatasetQuery:
        """
        Return draws containing at least one of the given Numbers.
        """
        return self._wrap(
            contains_any(
                self._dataset,
                *numbers,
            )
        )

    def contains_all(
        self,
        *numbers: Number,
    ) -> DatasetQuery:
        """
        Return draws containing all of the given Numbers.
        """
        return self._wrap(
            contains_all(
                self._dataset,
                *numbers,
            )
        )

    # ------------------------------------------------------------------
    # Combination queries
    # ------------------------------------------------------------------

    def matches(
        self,
        combination: Combination,
        *,
        at_least: int,
    ) -> DatasetQuery:
        """
        Return draws matching at least the requested number of values.

        Parameters
        ----------
        combination:
            Combination to compare against each Draw.
        at_least:
            Minimum number of matching values.
            Must be between 1 and 6 inclusive.

        Raises
        ------
        ValueError
            If ``at_least`` is outside the valid range.
        """
        return self._wrap(
            matches(
                self._dataset,
                combination,
                at_least=at_least,
            )
        )

    def intersects(
        self,
        combination: Combination,
    ) -> DatasetQuery:
        """
        Return draws sharing at least one Number.
        """
        return self._wrap(
            intersects(
                self._dataset,
                combination,
            )
        )

    def contains_exactly(
        self,
        combination: Combination,
    ) -> DatasetQuery:
        """
        Return draws matching every Number in the Combination.
        """
        return self._wrap(
            contains_exactly(
                self._dataset,
                combination,
            )
        )

    # ------------------------------------------------------------------
    # Generic predicate
    # ------------------------------------------------------------------

    def where(
        self,
        predicate: Callable[[Draw], bool],
    ) -> DatasetQuery:
        """
        Return draws matching the given predicate.
        """
        return self._select(predicate)

    filter = where
