"""
BaseBuilder.

Defines the common lifecycle shared by all builders.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar

T = TypeVar("T")


class BaseBuilder(ABC, Generic[T]):
    """
    Abstract base class for fluent builders.

    Lifecycle::

        builder = ConcreteBuilder()
        builder.add(...)
        builder.clear()
        builder.build()

    Builders are reusable.
    """

    @abstractmethod
    def build(self) -> T:
        """
        Build the target immutable object.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        Restore the builder to its initial state.
        """
        raise NotImplementedError

    def clear(self) -> Self:
        """
        Fluent alias for reset().

        Returns
        -------
        Self
            The builder itself.
        """
        self.reset()
        return self
