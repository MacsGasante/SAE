"""
Kernel Foundation.

Primitive building blocks shared by the entire Domain Model.

Foundation must never depend on higher-level Kernel packages.
"""

from .number import Number

__all__ = [
    "Number",
]
