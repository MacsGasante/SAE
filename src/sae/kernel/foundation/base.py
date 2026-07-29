"""
Kernel base abstractions.

These classes provide semantic meaning for the Domain Model while
remaining intentionally lightweight.

The Kernel favours composition over inheritance.
"""

from __future__ import annotations

from abc import ABC


class ValueObject(ABC):
    """
    Marker base class for immutable Value Objects.

    Concrete implementations should normally use:

        @dataclass(frozen=True, slots=True)

    Equality and hashing are delegated to the dataclass implementation.
    """

    __slots__ = ()


class Entity(ABC):
    """
    Marker base class for domain entities.

    Entities are identified by identity rather than value.
    """

    __slots__ = ()


class AggregateRoot(Entity):
    """
    Marker base class for Aggregate Roots.
    """

    __slots__ = ()
