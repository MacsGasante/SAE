"""
Kernel exception hierarchy.

All domain exceptions raised by the Kernel derive from SAEError.
"""

from __future__ import annotations

__all__ = [
    "SAEError",
    "KernelError",
    "DomainValidationError",
    "InvalidNumberError",
    "InvalidCombinationError",
]


class SAEError(Exception):
    """Base class for all SAE exceptions."""


class KernelError(SAEError):
    """Base class for Kernel exceptions."""


class DomainValidationError(KernelError):
    """Raised when a domain invariant is violated."""


class InvalidNumberError(DomainValidationError):
    """Raised when an invalid SuperEnalotto number is created."""


class InvalidCombinationError(DomainValidationError):
    """Raised when an invalid Combination is created."""
