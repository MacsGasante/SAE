"""
DrawId Value Object.

Represents the logical identifier of a SuperEnalotto draw.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..foundation.base import ValueObject
from .exceptions import InvalidDrawIdError


@dataclass(frozen=True, slots=True, order=True)
class DrawId(ValueObject):
    """
    Immutable Value Object representing a draw identifier.
    """

    value: int

    def __post_init__(self) -> None:
        self._validate_type()
        self._validate_value()

    def _validate_type(self) -> None:
        """
        Validate the underlying value type.
        """
        if not isinstance(self.value, int):
            raise InvalidDrawIdError(
                f"DrawId value must be an integer, got {type(self.value).__name__}."
            )

    def _validate_value(self) -> None:
        """
        Validate the domain invariant.
        """
        if self.value <= 0:
            raise InvalidDrawIdError("DrawId must be greater than zero.")

    def to_int(self) -> int:
        """
        Return the underlying integer.
        """
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"DrawId({self.value})"
