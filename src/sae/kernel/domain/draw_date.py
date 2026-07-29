"""
DrawDate Value Object.

Represents the official date of a SuperEnalotto draw.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ..foundation.base import ValueObject
from .exceptions import InvalidDrawDateError


@dataclass(frozen=True, slots=True, order=True)
class DrawDate(ValueObject):
    """
    Immutable Value Object representing the date of a draw.
    """

    value: date

    def __post_init__(self) -> None:
        self._validate_type()

    def _validate_type(self) -> None:
        """
        Validate the underlying value type.
        """
        if not isinstance(self.value, date):
            raise InvalidDrawDateError(
                f"DrawDate value must be a date, got {type(self.value).__name__}."
            )

    @classmethod
    def from_date(cls, value: date) -> DrawDate:
        """
        Create a DrawDate from an existing date object.
        """
        return cls(value)

    @classmethod
    def from_parts(
        cls,
        year: int,
        month: int,
        day: int,
    ) -> DrawDate:
        """
        Construct a DrawDate from year, month and day.
        """
        try:
            return cls(date(year, month, day))
        except ValueError as exc:
            raise InvalidDrawDateError(str(exc)) from exc

    @property
    def year(self) -> int:
        return self.value.year

    @property
    def month(self) -> int:
        return self.value.month

    @property
    def day(self) -> int:
        return self.value.day

    def to_date(self) -> date:
        """
        Return the underlying date object.
        """
        return self.value

    def isoformat(self) -> str:
        """
        Return the ISO-8601 representation.
        """
        return self.value.isoformat()

    def __str__(self) -> str:
        return self.isoformat()

    def __repr__(self) -> str:
        return f"DrawDate({self.isoformat()})"
