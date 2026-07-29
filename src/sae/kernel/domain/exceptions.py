"""
Domain-specific exceptions.
"""

from __future__ import annotations

from ..exceptions import DomainValidationError

__all__ = [
    "InvalidDrawIdError",
    "InvalidDrawDateError",
    "InvalidDrawError",
]


class InvalidDrawIdError(DomainValidationError):
    """
    Raised when a DrawId is not valid.
    """


class InvalidDrawDateError(DomainValidationError):
    """
    Raised when a DrawDate is not valid.
    """


class InvalidDrawError(DomainValidationError):
    """
    Raised when a Draw Aggregate cannot be created.
    """
