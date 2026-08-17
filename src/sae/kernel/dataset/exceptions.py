"""
Dataset-specific exceptions.
"""

from __future__ import annotations

from ..exceptions import DomainValidationError

__all__ = [
    "InvalidDatasetError",
]


class InvalidDatasetError(DomainValidationError):
    """
    Raised when a Dataset cannot be created.
    """
