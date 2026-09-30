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

    A DrawId can be created directly from a positive integer or
    deterministically from the official SuperEnalotto draw identity
    ``(year, contest_number)``.

    The official identity is transformed into a global integer using
    the following formula:

        DrawId = year * 1000 + contest_number

    This transformation is deterministic and preserves chronological
    ordering across years and within each year.
    """

    value: int

    def __post_init__(self) -> None:
        self._validate_type()
        self._validate_value()

    @classmethod
    def from_official(
        cls,
        year: int,
        contest_number: int,
    ) -> DrawId:
        """
        Create a DrawId from the official draw identity.

        Parameters
        ----------
        year:
            Official calendar year of the draw.
        contest_number:
            Official contest number within the year.
            Must be between 1 and 999.

        Returns
        -------
        DrawId
            Globally unique deterministic identifier.

        Raises
        ------
        InvalidDrawIdError
            If either input is not an integer or if
            ``contest_number`` is not greater than zero.

        Notes
        -----
        The transformation is:

            DrawId = year * 1000 + contest_number

        The official pair ``(year, contest_number)`` remains the
        authoritative source identity; the resulting DrawId is the
        internal global identifier used by the domain model.
        """
        if type(year) is not int:
            raise InvalidDrawIdError("DrawId year must be an integer.")

        if type(contest_number) is not int:
            raise InvalidDrawIdError("DrawId contest number must be an integer.")

        if not 1 <= contest_number < 1000:
            raise InvalidDrawIdError("DrawId contest number must be between 1 and 999.")

        return cls(
            year * 1000 + contest_number,
        )

    def _validate_type(self) -> None:
        """
        Validate the underlying value type.
        """
        if type(self.value) is not int:
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
