"""
SAE Kernel.

The Kernel contains the immutable Domain Model and the
fundamental abstractions used throughout the SAE project.

Packages
--------
foundation
    Primitive Value Objects and shared abstractions.

collections
    Immutable domain collections.

The Kernel must remain independent from infrastructure,
analytics and persistence layers.
"""

from .collections import Combination
from .exceptions import (
    DomainValidationError,
    InvalidCombinationError,
    InvalidNumberError,
    KernelError,
    SAEError,
)
from .foundation import Number

__all__ = [
    "SAEError",
    "KernelError",
    "DomainValidationError",
    "InvalidNumberError",
    "InvalidCombinationError",
    "Number",
    "Combination",
]
