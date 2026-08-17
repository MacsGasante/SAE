"""
Draw Aggregate Root.

Represents one official SuperEnalotto draw.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..collections import Combination
from ..foundation import Number
from ..foundation.base import AggregateRoot
from ._matching import compute_match
from .draw_date import DrawDate
from .draw_id import DrawId
from .exceptions import InvalidDrawError

if TYPE_CHECKING:
    from .match_result import MatchResult


class Draw(AggregateRoot):
    """
    Aggregate Root representing one official SuperEnalotto draw.

    Equality is identity-based (DrawId).
    """

    __slots__ = (
        "_id",
        "_date",
        "_combination",
    )

    def __init__(
        self,
        id: DrawId,
        date: DrawDate,
        combination: Combination,
    ) -> None:
        self._validate(
            id,
            date,
            combination,
        )

        object.__setattr__(
            self,
            "_id",
            id,
        )
        object.__setattr__(
            self,
            "_date",
            date,
        )
        object.__setattr__(
            self,
            "_combination",
            combination,
        )

    def __setattr__(
        self,
        name: str,
        value: object,
    ) -> None:
        """
        Prevent mutation after construction.
        """
        raise AttributeError(f"{type(self).__name__} is immutable.")

    @staticmethod
    def _validate(
        id: DrawId,
        date: DrawDate,
        combination: Combination,
    ) -> None:
        if not isinstance(
            id,
            DrawId,
        ):
            raise InvalidDrawError("id must be a DrawId.")

        if not isinstance(
            date,
            DrawDate,
        ):
            raise InvalidDrawError("date must be a DrawDate.")

        if not isinstance(
            combination,
            Combination,
        ):
            raise InvalidDrawError("combination must be a Combination.")

    @property
    def id(self) -> DrawId:
        """
        Return the draw identifier.
        """
        return self._id

    @property
    def date(self) -> DrawDate:
        """
        Return the draw date.
        """
        return self._date

    @property
    def combination(self) -> Combination:
        """
        Return the winning combination.
        """
        return self._combination

    @property
    def numbers(self) -> tuple[Number, ...]:
        """
        Return the draw numbers.
        """
        return self._combination.numbers

    def contains(
        self,
        number: Number,
    ) -> bool:
        """
        Return True if the given number belongs to the draw.
        """
        return number in self._combination

    def __eq__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(
            other,
            Draw,
        ):
            return NotImplemented

        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Draw(id={self.id}, date={self.date}, combination={self.combination})"

    def matches(
        self,
        combination: Combination,
    ) -> MatchResult:
        """
        Compute the matching Numbers between this Draw and a Combination.

        Returns
        -------
        MatchResult
            Immutable description of the matching Numbers.
        """
        return compute_match(
            self,
            combination,
        )
