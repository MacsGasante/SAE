"""
Combination Value Object.

Represents an immutable mathematical combination of distinct
SuperEnalotto numbers.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from ..exceptions import InvalidCombinationError
from ..foundation.base import ValueObject
from ..foundation.constants import COMBINATION_SIZE
from ..foundation.number import Number


@dataclass(frozen=True, slots=True, init=False)
class Combination(ValueObject):
    """
    Immutable collection of distinct Number objects.

    Numbers are always stored in ascending order.
    """

    _numbers: tuple[Number, ...]

    def __init__(self, *numbers: Number) -> None:
        self._validate_type(numbers)
        self._validate_cardinality(numbers)

        ordered = tuple(sorted(numbers))

        self._validate_duplicates(ordered)

        object.__setattr__(self, "_numbers", ordered)

    @staticmethod
    def _validate_type(numbers: tuple[Number, ...]) -> None:
        if not all(isinstance(number, Number) for number in numbers):
            raise InvalidCombinationError("All elements must be Number instances.")

    @staticmethod
    def _validate_cardinality(numbers: tuple[Number, ...]) -> None:
        if len(numbers) != COMBINATION_SIZE:
            raise InvalidCombinationError(
                f"Combination must contain exactly {COMBINATION_SIZE} numbers."
            )

    @staticmethod
    def _validate_duplicates(numbers: tuple[Number, ...]) -> None:
        if len(set(numbers)) != len(numbers):
            raise InvalidCombinationError("Duplicate numbers are not allowed.")

    @property
    def numbers(self) -> tuple[Number, ...]:
        """Return the numbers in ascending order."""
        return self._numbers

    @property
    def size(self) -> int:
        """Return the cardinality of the combination."""
        return len(self._numbers)

    @property
    def minimum(self) -> Number:
        """Return the smallest number."""
        return self._numbers[0]

    @property
    def maximum(self) -> Number:
        """Return the largest number."""
        return self._numbers[-1]

    def __iter__(self) -> Iterator[Number]:
        return iter(self._numbers)

    def __len__(self) -> int:
        return self.size

    def __contains__(self, item: object) -> bool:
        return item in self._numbers

    def __repr__(self) -> str:
        values = ", ".join(str(number) for number in self._numbers)
        return f"Combination({values})"
