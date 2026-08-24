"""
Domain matching helpers.

Private pure functions implementing matching logic between a Draw
and a Combination.

The public API is exposed by Draw.matches().
"""

from typing import TYPE_CHECKING

from ..collections import Combination
from ..foundation import Number
from .match_result import MatchResult

if TYPE_CHECKING:
    from .draw import Draw


def matching_numbers(
    draw: "Draw",
    combination: Combination,
) -> tuple[Number, ...]:
    """
    Return the Numbers shared by Draw and Combination.

    Numbers are returned preserving the Draw order.
    """
    requested = combination.numbers_set

    return tuple(number for number in draw.numbers if number in requested)


def compute_match(
    draw: "Draw",
    combination: Combination,
) -> MatchResult:
    """
    Compute the MatchResult between a Draw and a Combination.
    """
    return MatchResult(
        matching_numbers(
            draw,
            combination,
        )
    )
