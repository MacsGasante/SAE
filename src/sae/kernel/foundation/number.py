"""
Number Value Object.

Represents a valid SuperEnalotto number.

A Number is an immutable primitive Value Object belonging to the
Kernel Foundation.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import InvalidNumberError
from .base import ValueObject
from .constants import MAX_NUMBER, MIN_NUMBER
from .types import NumberValue


@dataclass(frozen=True, slots=True, order=True)
class Number(ValueObject):
    """
    Immutable Value Object representing a valid SuperEnalotto number.
    """

    value: NumberValue

    def __post_init__(self) -> None:
        self._validate_type()
        self._validate_range()

    def _validate_type(self) -> None:
        """Validate the underlying value type."""
        if not isinstance(self.value, int):
            raise InvalidNumberError(
                f"Number value must be an integer, got {type(self.value).__name__}."
            )

    def _validate_range(self) -> None:
        """Validate the allowed domain range."""
        if not MIN_NUMBER <= self.value <= MAX_NUMBER:
            raise InvalidNumberError(
                f"Number value must be between "
                f"{MIN_NUMBER} and {MAX_NUMBER}, "
                f"got {self.value}."
            )

    def to_int(self) -> int:
        """Return the underlying integer value."""
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Number({self.value})"
