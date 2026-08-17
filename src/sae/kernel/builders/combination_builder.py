"""
CombinationBuilder.

Fluent Builder for immutable Combination objects.
"""

from __future__ import annotations

from collections.abc import Iterable

from ..collections import Combination
from ..foundation import Number
from .base_builder import BaseBuilder


class CombinationBuilder(BaseBuilder[Combination]):
    """
    Builder for immutable Combination instances.

    The builder preserves insertion order until build() is called.

    Validation is delegated to Combination.
    """

    _numbers: list[Number]

    def __init__(self) -> None:
        self.reset()

    @property
    def numbers(self) -> tuple[Number, ...]:
        """
        Return the currently accumulated numbers.

        A tuple is returned to prevent external mutation.
        """
        return tuple(self._numbers)

    def add(self, number: Number) -> CombinationBuilder:
        """
        Append one Number.

        Returns
        -------
        CombinationBuilder
            The builder itself.
        """
        self._numbers.append(number)
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
        self._numbers.extend(numbers)
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

    def build(self) -> Combination:
        """
        Build an immutable Combination.

        Validation is entirely delegated to Combination.
        """
        return Combination(*self._numbers)

    def reset(self) -> None:
        """
        Reset the builder to its initial empty state.
        """
        self._numbers = []
