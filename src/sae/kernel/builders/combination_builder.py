"""
Combination Builder.

Provides a convenient API for constructing immutable Combination
instances.

Builders never perform domain validation.

Validation is entirely delegated to Combination.
"""

from __future__ import annotations

from collections.abc import Iterable

from ..collections.combination import Combination
from ..foundation.base import ValueObject
from ..foundation.number import Number
from .base_builder import BaseBuilder


class CombinationBuilder(BaseBuilder):
    """
    Builder for immutable Combination objects.

    The builder stores temporary construction state while delegating
    every validation rule to Combination.
    """

    def __init__(self) -> None:
        self.reset()

    @property
    def numbers(self) -> tuple[Number, ...]:
        """
        Return the current builder content.

        This property is intended for inspection and testing.
        """
        return self._numbers

    def add(self, number: Number) -> CombinationBuilder:
        """
        Append a Number to the builder.

        Returns
        -------
        CombinationBuilder
            The builder itself to support fluent usage.
        """
        self._numbers = (*self._numbers, number)
        return self

    def extend(
        self,
        numbers: Iterable[Number],
    ) -> CombinationBuilder:
        """
        Append multiple numbers.

        Returns
        -------
        CombinationBuilder
            The builder itself.
        """
        self._numbers = (*self._numbers, *tuple(numbers))
        return self

    @classmethod
    def from_numbers(
        cls,
        *numbers: Number,
    ) -> CombinationBuilder:
        """
        Create a builder already populated with numbers.
        """
        builder = cls()
        builder.extend(numbers)
        return builder

    def reset(self) -> None:
        """
        Reset the builder.
        """
        self._numbers: tuple[Number, ...] = ()

    def build(self) -> ValueObject:
        """
        Build a Combination.

        Returns
        -------
        ValueObject

        Raises
        ------
        InvalidCombinationError
            Propagated directly from Combination whenever the current
            builder state is invalid.
        """
        return Combination(*self._numbers)
