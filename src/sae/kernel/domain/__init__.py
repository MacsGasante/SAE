"""
Domain Model.

This package contains the Aggregate Roots and Value Objects
representing the SuperEnalotto domain.
"""

from .draw import Draw
from .draw_date import DrawDate
from .draw_id import DrawId
from .match_result import MatchResult

__all__ = [
    "Draw",
    "DrawDate",
    "DrawId",
    "MatchResult",
]
