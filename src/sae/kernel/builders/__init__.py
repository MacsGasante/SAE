"""
Kernel Builder Framework.

Builders provide convenient construction APIs for immutable
Domain Objects.

Builders never implement business rules.

Validation always belongs to the target Domain Object.
"""

from .base_builder import BaseBuilder
from .combination_builder import CombinationBuilder

__all__ = [
    "BaseBuilder",
    "CombinationBuilder",
]
