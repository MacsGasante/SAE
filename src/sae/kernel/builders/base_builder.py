"""
Kernel Builder Framework.

This module defines the abstract base class shared by all Kernel builders.

Builders are responsible only for collecting construction data and
creating immutable Domain Objects.

Builders never implement business rules or domain validation.

Every validation is delegated to the target Domain Object.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..foundation.base import ValueObject


class BaseBuilder(ABC):
    """
    Base class for all SAE builders.

    Builders expose a convenient API for constructing immutable
    Domain Objects while delegating every domain invariant to the
    resulting Value Object.

    Builder lifecycle
    -----------------
    Typical usage::

        builder.add(...)
        builder.add(...)
        ...
        result = builder.build()

    Builders are reusable.

    Calling build() never resets the builder automatically.

    Use reset() (or clear()) explicitly to discard the current state.

    Notes
    -----
    Builders never validate domain invariants.

    Every validation is delegated to the constructed Domain Object.
    """

    __slots__ = ()

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the internal builder state.
        """

    def clear(self) -> None:
        """
        Alias of reset().

        The two names express different intentions while performing the
        same operation.
        """
        self.reset()

    @abstractmethod
    def build(self) -> ValueObject:
        """
        Build the target Value Object.

        Returns
        -------
        ValueObject
            A newly created immutable Domain Object.

        Notes
        -----
        Concrete builders delegate every validation to the constructed
        Domain Object.
        """
