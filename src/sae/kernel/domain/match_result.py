"""
Match Result.

Immutable Value Object representing the outcome of a match operation.

A MatchResult contains the Numbers shared between a Draw and a
requested collection of Numbers.

It is intentionally independent from DatasetQuery and the query
algorithms so that it can be reused by future Statistics,
Evidence and Pattern engines.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from sae.kernel.foundation import Number
from sae.kernel.foundation.constants import COMBINATION_SIZE


@dataclass(frozen=True, slots=True)
class MatchResult:
    """
    Immutable result of a match operation.

    Parameters
    ----------
    numbers:
        Matching Numbers, in Draw order.
    """

    _numbers: tuple[Number, ...]

    def __post_init__(self) -> None:
        """
        Validate the MatchResult invariants.
        """
        self._validate_type()
        self._validate_numbers()

    def _validate_type(self) -> None:
        """
        Validate the underlying collection type.
        """
        if type(self._numbers) is not tuple:
            raise TypeError("MatchResult numbers must be a tuple.")

    def _validate_numbers(self) -> None:
        """
        Validate the matching Numbers.
        """
        if len(self._numbers) > COMBINATION_SIZE:
            raise ValueError(
                f"MatchResult cannot contain more than {COMBINATION_SIZE} Numbers."
            )

        for number in self._numbers:
            if not isinstance(number, Number):
                raise TypeError("MatchResult can contain only Number instances.")

    @property
    def numbers(self) -> tuple[Number, ...]:
        """
        Matching Numbers.
        """
        return self._numbers

    @property
    def count(self) -> int:
        """
        Number of matching Numbers.
        """
        return len(self._numbers)

    @property
    def is_empty(self) -> bool:
        """
        Return True if no Numbers matched.
        """
        return self.count == 0

    @property
    def matched(self) -> bool:
        """
        Return True if at least one Number matched.
        """
        return self.count > 0

    @property
    def is_exact(self) -> bool:
        """
        Return True if all combination Numbers matched.
        """
        return self.count == COMBINATION_SIZE

    @property
    def ratio(self) -> float:
        """
        Matching ratio in the interval [0.0, 1.0].
        """
        return self.count / COMBINATION_SIZE

    def __len__(self) -> int:
        """
        Return the number of matching Numbers.
        """
        return self.count

    def __bool__(self) -> bool:
        """
        Truth value of the MatchResult.

        A MatchResult evaluates to True when at least one Number
        matched.
        """
        return self.matched

    def __iter__(self) -> Iterator[Number]:
        """
        Iterate over the matching Numbers.
        """
        return iter(self._numbers)

    def __contains__(
        self,
        number: Number,
    ) -> bool:
        return number in self._numbers
